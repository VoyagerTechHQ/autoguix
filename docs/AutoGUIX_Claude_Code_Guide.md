# AutoGUI-X for macOS - Claude Code 协作指南

**版本**: 1.0  
**目标**: 提供具体的 Claude Code 提示词模板和协作流程,确保高效开发。

---

## 1. 协作流程

### 1.1. 初始化项目

**提示词模板**:

```
我正在开发一个名为 AutoGUI-X 的 macOS GUI 自动化库。请帮我初始化项目结构。

项目要求:
- 使用 uv 作为包管理工具
- Python 3.8+
- 项目名称: autoguix
- 使用 pyproject.toml

请执行以下操作:
1. 创建项目目录结构
2. 生成 pyproject.toml 文件,使用现代的 [project] 语法,包含以下依赖:
   - Pillow>=10.0.0
   - numpy>=1.24.0
   - pyobjc-core>=10.0 (仅 macOS)
   - pyobjc-framework-Quartz>=10.0 (仅 macOS)
   - pyobjc-framework-ApplicationServices>=10.0 (仅 macOS)
3. 创建以下目录和空文件:
   - autoguix/
   - autoguix/__init__.py
   - autoguix/core/
   - autoguix/core/__init__.py
   - autoguix/core/types.py
   - autoguix/core/backend_base.py
   - autoguix/core/automation_core.py
   - autoguix/backends/
   - autoguix/backends/__init__.py
   - autoguix/backends/macos_backend.py
   - examples/
   - examples/macos_demo.py
   - tests/
   - README.md
   - LICENSE
```

---

### 1.2. 阶段 1: 核心数据类型

**提示词模板**:

```
请为 AutoGUI-X 项目实现核心数据类型。

文件: autoguix/core/types.py

要求:
1. 使用 typing.NamedTuple 定义以下类:
   - Point: x (int), y (int)
   - Size: width (int), height (int)
   - Region: left (int), top (int), width (int), height (int)

2. 使用 enum.Enum 定义以下枚举:
   - MouseButton: LEFT, RIGHT, MIDDLE
   - LocateMode: IMAGE, OBJECT

3. 为所有类添加 docstrings (Google 风格)

4. 确保所有类型都可以被导出 (__all__)
```

---

### 1.3. 阶段 1: 后端抽象基类

**提示词模板**:

```
请为 AutoGUI-X 项目实现后端抽象基类。

文件: autoguix/core/backend_base.py

要求:
1. 创建 BackendBase 抽象基类,继承自 abc.ABC

2. 定义以下抽象方法 (全部使用 @abstractmethod 和 async):
   
   初始化:
   - async def initialize(self) -> None
   - async def cleanup(self) -> None
   
   鼠标操作:
   - async def get_mouse_position(self) -> Point
   - async def move_mouse(self, x: int, y: int, duration: float = 0.0) -> None
   - async def click(self, x: Optional[int] = None, y: Optional[int] = None, 
                     button: MouseButton = MouseButton.LEFT, clicks: int = 1, 
                     interval: float = 0.0) -> None
   
   键盘操作:
   - async def press_key(self, key: str) -> None
   - async def key_down(self, key: str) -> None
   - async def key_up(self, key: str) -> None
   - async def type_text(self, text: str, interval: float = 0.0) -> None
   
   屏幕操作:
   - async def get_screen_size(self) -> Tuple[int, int]
   - async def take_screenshot(self, region: Optional[Region] = None) -> Image.Image
   
   定位操作:
   - async def locate_on_screen(self, image: str, confidence: float = 0.9, 
                                 region: Optional[Region] = None, 
                                 mode: LocateMode = LocateMode.IMAGE) -> Optional[Region]
   - async def locate_all_on_screen(self, image: str, confidence: float = 0.9, 
                                     region: Optional[Region] = None, 
                                     mode: LocateMode = LocateMode.IMAGE) -> List[Region]

3. 为类和所有方法添加详细的 docstrings (Google 风格)

4. 导入必要的类型: Point, Size, Region, MouseButton, LocateMode, Optional, Tuple, List, Image
```

---

### 1.4. 阶段 2: macOS 后端 - 屏幕和鼠标

**提示词模板**:

```
请为 AutoGUI-X 项目实现 macOS 后端的屏幕和鼠标操作。

文件: autoguix/backends/macos_backend.py

上下文:
- 这个类继承自 BackendBase
- 使用 PyObjC 调用 macOS 原生 API
- 需要实现懒加载 Quartz 框架

要求:
1. 创建 MacOSBackend 类,继承自 BackendBase

2. 实现 __init__ 方法:
   - 初始化 _quartz_loaded = False
   - 接受可选的 config 参数

3. 实现 _load_quartz 私有方法:
   - 懒加载 Quartz 框架
   - 从 Quartz 导入所需的常量和函数
   - 设置 _quartz_loaded = True
   - 如果导入失败,抛出 RuntimeError 并提示安装 pyobjc-framework-Quartz

4. 实现以下方法:
   
   a) async def initialize(self) -> None
      - 调用 _load_quartz
      - 设置 _initialized = True
   
   b) async def get_screen_size(self) -> Tuple[int, int]
      - 使用 CGDisplayBounds(CGMainDisplayID())
      - 返回 (width, height)
   
   c) async def get_mouse_position(self) -> Point
      - 使用 CGEventGetLocation(CGEventCreate(None))
      - 返回 Point 对象
   
   d) async def move_mouse(self, x: int, y: int, duration: float = 0.0) -> None
      - 使用 CGEventCreateMouseEvent 和 kCGEventMouseMoved
      - 如果 duration > 0, 实现平滑移动 (线性插值)
      - 使用 CGEventPost 发送事件
   
   e) async def click(self, x: Optional[int] = None, y: Optional[int] = None, 
                      button: MouseButton = MouseButton.LEFT, clicks: int = 1, 
                      interval: float = 0.0) -> None
      - 如果提供了 x, y, 先调用 move_mouse
      - 根据 button 选择对应的事件类型
      - 使用 CGEventCreateMouseEvent 和 CGEventPost
      - 实现 clicks 和 interval

5. 为所有方法添加详细的 docstrings

6. 使用 asyncio.get_event_loop().run_in_executor 包装同步操作
```

---

### 1.5. 阶段 3: macOS 后端 - 键盘和截图

**提示词模板**:

```
请为 AutoGUI-X 项目实现 macOS 后端的键盘和截图操作。

文件: autoguix/backends/macos_backend.py (继续添加)

要求:
1. 实现 _get_keycode 私有方法:
   - 创建一个字典,映射常用键名到 macOS keycode
   - 至少包含: a-z, 0-9, enter, tab, space, delete, escape, command, shift, control, option, 方向键, F1-F12
   - 如果键名未找到,抛出 ValueError

2. 实现键盘方法:
   
   a) async def key_down(self, key: str) -> None
      - 使用 CGEventCreateKeyboardEvent(None, keycode, True)
      - 使用 CGEventPost 发送事件
   
   b) async def key_up(self, key: str) -> None
      - 使用 CGEventCreateKeyboardEvent(None, keycode, False)
      - 使用 CGEventPost 发送事件
   
   c) async def press_key(self, key: str) -> None
      - 调用 key_down
      - 等待 0.01 秒
      - 调用 key_up
   
   d) async def type_text(self, text: str, interval: float = 0.0) -> None
      - 遍历每个字符
      - 调用 press_key
      - 如果 interval > 0, 等待相应时间

3. 实现截图方法:
   
   async def take_screenshot(self, region: Optional[Region] = None) -> Image.Image
   - 使用 CGWindowListCreateImage
   - 如果提供了 region, 使用 CGRectMake 创建矩形
   - 否则使用 CGRectInfinite
   - 将 CGImage 转换为 PIL Image (BGRA -> RGB)
   - 使用 numpy 进行格式转换

4. 为所有方法添加详细的 docstrings
```

---

### 1.6. 阶段 4: 图像定位

**提示词模板**:

```
请为 AutoGUI-X 项目实现图像定位功能。

文件: autoguix/backends/macos_backend.py (继续添加)

要求:
1. 在 __init__ 中添加 _cv2 = None

2. 实现 _load_cv2 私有方法:
   - 懒加载 opencv-python
   - 如果导入失败,抛出 RuntimeError 并提示安装

3. 实现定位方法:
   
   a) async def locate_on_screen(self, image: str, confidence: float = 0.9, 
                                  region: Optional[Region] = None, 
                                  mode: LocateMode = LocateMode.IMAGE) -> Optional[Region]
      - 调用 _load_cv2
      - 调用 take_screenshot 获取屏幕图像
      - 使用 cv2.imread 加载模板图像
      - 转换为灰度图像
      - 使用 cv2.matchTemplate 和 TM_CCOEFF_NORMED
      - 使用 cv2.minMaxLoc 找到最佳匹配
      - 如果 max_val >= confidence, 返回 Region
      - 否则返回 None
   
   b) async def locate_all_on_screen(self, image: str, confidence: float = 0.9, 
                                      region: Optional[Region] = None, 
                                      mode: LocateMode = LocateMode.IMAGE) -> List[Region]
      - (初版) 调用 locate_on_screen
      - 如果找到,返回包含一个 Region 的列表
      - 否则返回空列表

4. 为所有方法添加详细的 docstrings
```

---

### 1.7. 自动化核心和用户 API

**提示词模板**:

```
请为 AutoGUI-X 项目实现自动化核心和用户 API。

文件 1: autoguix/core/automation_core.py

要求:
1. 创建 AutomationCore 类

2. 实现 __init__ 方法:
   - 检测 sys.platform
   - 如果是 'darwin', 实例化 MacOSBackend
   - 否则抛出 RuntimeError (暂不支持其他平台)

3. 实现初始化方法:
   - async def initialize(self) -> None
   - def initialize_sync(self) -> None (使用 asyncio.run)

4. 为每个后端方法创建包装方法:
   - 同步版本 (e.g., click_sync)
   - 异步版本 (e.g., click_async)

---

文件 2: autoguix/__init__.py

要求:
1. 创建全局 _core 实例

2. 实现 init() 函数:
   - 调用 _core.initialize_sync()

3. 为每个核心功能创建用户函数:
   - 例如: def click(x=None, y=None, button='left', clicks=1, interval=0.0)
   - 调用 _core.click_sync(...)
   - 处理 button 参数 (字符串 -> MouseButton 枚举)

4. 实现以下函数 (PyAutoGUI 兼容):
   - size() -> Tuple[int, int]
   - position() -> Tuple[int, int]
   - moveTo(x, y, duration=0.0)
   - click(x=None, y=None, clicks=1, interval=0.0, button='left')
   - press(key)
   - typewrite(text, interval=0.0)
   - screenshot(imageFilename=None, region=None) -> Image.Image
   - locateOnScreen(image, confidence=0.9, region=None) -> Optional[Region]

5. 定义 __all__ 导出所有公共函数
```

---

## 2. 代码审查清单

在 Claude Code 生成代码后,使用以下清单进行审查:

- [ ] **类型提示**: 所有函数参数和返回值都有类型提示
- [ ] **Docstrings**: 所有公共函数和类都有 Google 风格的 docstrings
- [ ] **错误处理**: 适当的异常处理和错误消息
- [ ] **异步实现**: 正确使用 `async/await` 和 `asyncio`
- [ ] **懒加载**: PyObjC 和 OpenCV 使用懒加载
- [ ] **代码风格**: 符合 PEP 8
- [ ] **注释**: 复杂逻辑有清晰的注释
- [ ] **测试**: 可以编写单元测试

---

## 3. 常见问题和解决方案

### 3.1. PyObjC 导入错误

**问题**: `ImportError: No module named 'Quartz'`

**解决**: 
```python
try:
    from Quartz import ...
except ImportError as e:
    raise RuntimeError(
        "Failed to load Quartz framework. "
        "Please install pyobjc-framework-Quartz: "
        "pip install pyobjc-framework-Quartz"
    ) from e
```

### 3.2. 异步和同步混用

**问题**: 在同步上下文中调用异步方法

**解决**: 
```python
def sync_method(self):
    return asyncio.run(self.async_method())
```

或使用 `asyncio.get_event_loop().run_in_executor`:
```python
async def async_method(self):
    return await asyncio.get_event_loop().run_in_executor(
        None, self.sync_method
    )
```

### 3.3. CGImage 到 PIL Image 转换

**问题**: 图像格式转换复杂

**解决**: 
```python
from Quartz import CGImageGetWidth, CGImageGetHeight, CGImageGetDataProvider, CGDataProviderCopyData
import numpy as np
from PIL import Image

width = CGImageGetWidth(image_ref)
height = CGImageGetHeight(image_ref)
data_provider = CGImageGetDataProvider(image_ref)
data = CGDataProviderCopyData(data_provider)

import array
buf = array.array('B', data)
img_array = np.frombuffer(buf, dtype=np.uint8)
img_array = img_array.reshape((height, width, 4))
img_array = img_array[:, :, [2, 1, 0]]  # BGRA -> RGB

return Image.fromarray(img_array)
```

---

## 4. 测试和验证

### 4.1. 手动测试脚本

创建 `test_manual.py`:

```python
import autoguix as ag

# 初始化
ag.init()

# 测试屏幕尺寸
width, height = ag.size()
print(f"Screen size: {width}x{height}")

# 测试鼠标位置
x, y = ag.position()
print(f"Mouse position: ({x}, {y})")

# 测试鼠标移动
ag.moveTo(width // 2, height // 2, duration=1.0)
print("Moved mouse to center")

# 测试截图
screenshot = ag.screenshot()
screenshot.save("test_screenshot.png")
print("Screenshot saved")

# 测试输入 (需要手动打开文本编辑器)
input("Open a text editor and press Enter...")
ag.typewrite("Hello from AutoGUI-X!", interval=0.05)
print("Text typed")
```

### 4.2. 单元测试示例

创建 `tests/test_core.py`:

```python
import pytest
from autoguix.core.types import Point, Region, MouseButton

def test_point():
    p = Point(100, 200)
    assert p.x == 100
    assert p.y == 200

def test_region():
    r = Region(10, 20, 300, 400)
    assert r.left == 10
    assert r.top == 20
    assert r.width == 300
    assert r.height == 400

def test_mouse_button():
    assert MouseButton.LEFT.value == "left"
    assert MouseButton.RIGHT.value == "right"
```

---

**通过遵循这个指南,您可以高效地与 Claude Code 协作,完成 AutoGUI-X 项目的开发。**
