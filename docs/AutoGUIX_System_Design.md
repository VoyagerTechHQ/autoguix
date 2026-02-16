# AutoGUI-X for macOS - 系统设计文档

**版本**: 1.0  
**目标**: 为 Claude Code 提供清晰、结构化的系统设计,以便高效实现。

---

## 1. 核心设计原则

1.  **macOS 优先**: 所有设计决策都优先考虑 macOS 平台的最佳实践和性能。
2.  **模块化与可扩展**: 采用插件化架构,未来可以轻松扩展到其他平台。
3.  **API 兼容性**: 100% 兼容 PyAutoGUI 的核心 API,方便用户迁移。
4.  **现代化**: 全面拥抱异步 (`async/await`) 和类型提示。
5.  **可靠性**: 优先使用 macOS 原生 API (Quartz, Accessibility) 而非图像识别。

---

## 2. 系统架构: 三层插件化设计

AutoGUI-X 采用三层架构,将用户接口、核心逻辑和平台实现完全解耦。

**架构层次图**:

```
┌─────────────────────────────────────────────────────────┐
│  用户层 (User API Layer)                                │
│  autoguix/__init__.py                                   │
│  提供 PyAutoGUI 兼容的函数, 如 ag.click()                │
└────────────────────┬────────────────────────────────────┘
                     │ 调用
                     ↓
┌─────────────────────────────────────────────────────────┐
│  核心层 (Core Layer)                                     │
│  autoguix/core/automation_core.py                       │
│  管理后端实例, 处理异步/同步调用                          │
└────────────────────┬────────────────────────────────────┘
                     │ 加载并调用
                     ↓
┌─────────────────────────────────────────────────────────┐
│  后端层 (Backend Layer)                                  │
│  autoguix/backends/macos_backend.py                     │
│  实现平台相关的具体操作                                   │
└────────────────────┬────────────────────────────────────┘
                     │ 与系统交互
                     ↓
              ┌──────────────┐
              │  macOS API   │
              └──────────────┘
```

### 2.1. 用户层 (User API Layer)

- **文件**: `autoguix/__init__.py`
- **职责**: 
  - 提供用户直接调用的函数 (e.g., `autoguix.click()`, `autoguix.moveTo()`)。
  - 保持与 PyAutoGUI 的 API 签名一致。
  - 实例化并管理一个全局的 `AutomationCore` 对象。
  - 将同步和异步调用委托给 `AutomationCore`。

### 2.2. 核心层 (Core Layer)

- **文件**: `autoguix/core/automation_core.py`
- **职责**:
  - 在初始化时检测当前操作系统,并加载相应的后端 (e.g., `MacOSBackend`)。
  - 管理后端实例的生命周期 (`initialize`, `cleanup`)。
  - 提供同步和异步两种方法 (e.g., `click_sync`, `click_async`)。
  - 封装与平台无关的通用逻辑 (e.g., 平滑移动的插值计算)。

### 2.3. 后端层 (Backend Layer)

- **文件**: `autoguix/backends/macos_backend.py`
- **职责**:
  - 实现 `BackendBase` 抽象基类中定义的所有方法。
  - 调用特定于 macOS 的系统 API (通过 PyObjC)。
  - **鼠标/键盘**: 使用 `Quartz Event Services`。
  - **截图**: 使用 `Core Graphics`。
  - **对象识别**: 使用 `Accessibility API` (未来)。

---

## 3. 核心数据结构

定义在 `autoguix/core/types.py` (或类似文件)。

```python
from typing import NamedTuple
from enum import Enum

class Point(NamedTuple):
    x: int
    y: int

class Size(NamedTuple):
    width: int
    height: int

class Region(NamedTuple):
    left: int
    top: int
    width: int
    height: int

class MouseButton(Enum):
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"

class LocateMode(Enum):
    IMAGE = "image"
    OBJECT = "object"
```

---

## 4. 核心类和接口定义

### 4.1. `autoguix.core.backend_base.BackendBase` (抽象基类)

这个接口是所有平台后端必须实现的契约。

```python
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from PIL import Image
from .types import Point, Region, MouseButton, LocateMode

class BackendBase(ABC):
    @abstractmethod
    async def initialize(self) -> None:
        ...

    @abstractmethod
    async def cleanup(self) -> None:
        ...

    # --- Mouse --- #
    @abstractmethod
    async def get_mouse_position(self) -> Point:
        ...

    @abstractmethod
    async def move_mouse(self, x: int, y: int, duration: float) -> None:
        ...

    @abstractmethod
    async def click(self, x: Optional[int], y: Optional[int], button: MouseButton, clicks: int, interval: float) -> None:
        ...

    # --- Keyboard --- #
    @abstractmethod
    async def press_key(self, key: str) -> None:
        ...

    @abstractmethod
    async def key_down(self, key: str) -> None:
        ...

    @abstractmethod
    async def key_up(self, key: str) -> None:
        ...

    @abstractmethod
    async def type_text(self, text: str, interval: float) -> None:
        ...

    # --- Screen --- #
    @abstractmethod
    async def get_screen_size(self) -> Tuple[int, int]:
        ...

    @abstractmethod
    async def take_screenshot(self, region: Optional[Region]) -> Image.Image:
        ...

    # --- Location --- #
    @abstractmethod
    async def locate_on_screen(self, image: str, confidence: float, region: Optional[Region], mode: LocateMode) -> Optional[Region]:
        ...

    @abstractmethod
    async def locate_all_on_screen(self, image: str, confidence: float, region: Optional[Region], mode: LocateMode) -> List[Region]:
        ...
```

### 4.2. `autoguix.backends.macos_backend.MacOSBackend`

这个类将实现 `BackendBase` 中定义的所有方法,使用 PyObjC 调用 macOS 的原生 API。

- **`initialize`**: 动态加载 `Quartz` 和 `ApplicationServices` 框架。
- **`move_mouse`**: 使用 `CGEventCreateMouseEvent` 和 `kCGEventMouseMoved`。
- **`click`**: 使用 `CGEventCreateMouseEvent` 和 `kCGEventLeftMouseDown`/`kCGEventLeftMouseUp`。
- **`press_key`**: 使用 `CGEventCreateKeyboardEvent`。
- **`take_screenshot`**: 使用 `CGWindowListCreateImage`。
- **`locate_on_screen`**: 结合 `take_screenshot` 和 `opencv-python` 进行模板匹配。

---

## 5. 项目文件结构

```
autoguix/
├── autoguix/                  # 主要源代码目录
│   ├── __init__.py            # 用户 API 层, e.g., ag.click()
│   ├── core/                  # 核心逻辑
│   │   ├── __init__.py
│   │   ├── automation_core.py # 自动化核心管理器
│   │   ├── backend_base.py    # 后端抽象基类
│   │   └── types.py           # 核心数据结构
│   └── backends/              # 平台后端
│       ├── __init__.py
│       └── macos_backend.py   # macOS 后端实现
├── examples/
│   └── macos_demo.py          # 示例代码
├── tests/
│   ├── test_core.py
│   └── test_macos_backend.py
├── pyproject.toml             # 项目配置和依赖
├── README.md
└── LICENSE
```

---
### 6. 依赖管理

使用 `pyproject.toml` 和 **`uv`** 作为包管理工具。uv 是一个极快的 Python 包管理器,由 Rust 编写。

- **核心依赖**: `Pillow`, `numpy`
- **macOS 特定依赖**: `pyobjc-core`, `pyobjc-framework-Quartz`, `pyobjc-framework-ApplicationServices`
- **可选依赖 (图像识别)**: `opencv-python`

```toml
# pyproject.toml

[project]
name = "autoguix"
version = "0.1.0"
description = "Modern macOS GUI automation library for Python"
authors = [{name = "Your Name", email = "your.email@example.com"}]
requires-python = ">=3.8"
readme = "README.md"
license = {text = "BSD-3-Clause"}

dependencies = [
    "Pillow>=10.0.0",
    "numpy>=1.24.0",
    "pyobjc-core>=10.0; sys_platform == 'darwin'",
    "pyobjc-framework-Quartz>=10.0; sys_platform == 'darwin'",
    "pyobjc-framework-ApplicationServices>=10.0; sys_platform == 'darwin'",
]

[project.optional-dependencies]
locate = [
    "opencv-python>=4.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

**下一步**: 开发计划和实现指南,将详细说明如何一步步实现上述设计。
