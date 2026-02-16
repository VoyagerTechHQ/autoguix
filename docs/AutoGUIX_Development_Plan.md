# AutoGUI-X for macOS - 开发计划与实现指南

**版本**: 1.0  
**目标**: 为 Claude Code 提供分步实现指南,确保代码质量和一致性。

---

## 1. 开发环境设置

1.  **安装 uv**: 
    ```bash
    # macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # 或使用 pip
    pip install uv
    ```

2.  **创建项目**:
    ```bash
    mkdir autoguix
    cd autoguix
    uv init
    ```

3.  **创建 pyproject.toml**: 使用系统设计文档中的配置。

4.  **安装依赖**:
    ```bash
    # 安装核心依赖
    uv pip install -e .
    
    # 安装可选依赖 (图像定位)
    uv pip install -e ".[locate]"
    ```

5.  **创建文件结构**: 按照系统设计文档创建目录和文件。

---

## 2. 开发计划 (分阶段实现)

### **阶段 1: 核心架构和数据类型 (预计 1-2 小时)**

**目标**: 搭建项目骨架,定义核心数据结构和接口。

1.  **`autoguix/core/types.py`**:
    - 实现 `Point`, `Size`, `Region`, `MouseButton`, `LocateMode`。
    - 使用 `NamedTuple` 和 `Enum`。

2.  **`autoguix/core/backend_base.py`**:
    - 创建 `BackendBase` 抽象基类。
    - 定义所有抽象方法 (`@abstractmethod`),使用类型提示。
    - 所有方法都应是 `async`。

3.  **`autoguix/backends/macos_backend.py`**:
    - 创建 `MacOSBackend` 类,继承自 `BackendBase`。
    - 实现所有方法的存根 (e.g., `raise NotImplementedError`)。

4.  **`autoguix/core/automation_core.py`**:
    - 创建 `AutomationCore` 类。
    - 在 `__init__` 中检测 `sys.platform` 并实例化 `MacOSBackend`。
    - 实现 `initialize` 和 `cleanup` 方法,调用后端的相应方法。

5.  **`autoguix/__init__.py`**:
    - 创建一个全局的 `_core = AutomationCore()` 实例。
    - 定义一个 `init()` 函数,调用 `_core.initialize()`。
    - 定义一个 `size()` 函数作为示例,调用 `_core.get_screen_size()`。

**验收标准**: 可以成功导入 `autoguix` 并调用 `autoguix.init()` 和 `autoguix.size()` (即使后者会抛出 `NotImplementedError`)。

---

### **阶段 2: 屏幕和鼠标操作 (预计 3-4 小时)**

**目标**: 实现核心的屏幕信息获取和鼠标控制功能。

1.  **`MacOSBackend.get_screen_size`**:
    - 使用 `CGDisplayBounds(CGMainDisplayID())`。
    - 返回 `(width, height)` 元组。

2.  **`MacOSBackend.get_mouse_position`**:
    - 使用 `CGEventGetLocation(CGEventCreate(None))`。
    - 返回 `Point` 对象。

3.  **`MacOSBackend.move_mouse`**:
    - 使用 `CGEventCreateMouseEvent` 和 `kCGEventMouseMoved`。
    - 实现 `duration` 参数,用于平滑移动 (使用 `time.sleep` 和线性插值)。

4.  **`MacOSBackend.click`**:
    - 如果提供了 `x, y`, 先调用 `move_mouse`。
    - 根据 `button` 参数选择 `kCGEventLeftMouseDown/Up`, `kCGEventRightMouseDown/Up` 等。
    - 使用 `CGEventCreateMouseEvent` 和 `CGEventPost` 发送事件。
    - 实现 `clicks` 和 `interval` 参数。

5.  **更新 `AutomationCore` 和 `__init__.py`**:
    - 为上述功能添加相应的同步和异步方法。
    - 例如, `click()` (同步) 和 `click_async()` (异步)。

**验收标准**: 可以通过 `autoguix` 控制鼠标移动和点击,获取屏幕尺寸和鼠标位置。

---

### **阶段 3: 键盘和截图操作 (预计 2-3 小时)**

**目标**: 实现键盘输入和屏幕截图功能。

1.  **`MacOSBackend._get_keycode`**:
    - 创建一个字典,映射常用键名 (e.g., 'a', 'enter', 'f1') 到 macOS keycode。
    - 这是一个私有辅助方法。

2.  **`MacOSBackend.press_key`, `key_down`, `key_up`**:
    - 使用 `CGEventCreateKeyboardEvent` 和 `CGEventPost`。
    - `press_key` 调用 `key_down` 和 `key_up`。

3.  **`MacOSBackend.type_text`**:
    - 遍历输入字符串的每个字符。
    - 调用 `press_key` 模拟输入。
    - 实现 `interval` 参数。

4.  **`MacOSBackend.take_screenshot`**:
    - 使用 `CGWindowListCreateImage`。
    - 将返回的 `CGImage` 转换为 `PIL.Image` 对象 (这部分比较复杂,需要处理像素格式 BGRA -> RGB)。
    - 支持 `region` 参数。

5.  **更新 `AutomationCore` 和 `__init__.py`**。

**验收标准**: 可以通过 `autoguix` 输入文本和进行截图。

---

### **阶段 4: 图像定位 (预计 2-3 小时)**

**目标**: 实现屏幕图像定位功能。

1.  **`MacOSBackend.locate_on_screen`**:
    - 调用 `take_screenshot` 获取屏幕图像。
    - 使用 `cv2.imread` 加载模板图像。
    - 使用 `cv2.matchTemplate` 进行模板匹配。
    - 如果匹配度 (`max_val`) 高于 `confidence`,返回 `Region` 对象。

2.  **`MacOSBackend.locate_all_on_screen`**:
    - (初版可以简化) 找到所有匹配度高于 `confidence` 的位置。
    - 返回 `List[Region]`。

3.  **更新 `AutomationCore` 和 `__init__.py`**。

**验收标准**: 可以成功在屏幕上定位一个已知图像。

---

### **阶段 5: 文档、测试和打包 (预计 3-4 小时)**

**目标**: 完善项目,准备发布。

1.  **文档**: 
    - 为所有公共函数和类编写详细的 docstrings (Google 风格)。
    - 编写 `README.md`,突出 macOS 优先的特点。

2.  **测试**: 
    - 使用 `pytest` 和 `pytest-asyncio`。
    - 编写单元测试 (mock 后端)。
    - 编写集成测试 (需要手动验证)。

3.  **示例**: 
    - 创建 `examples/macos_demo.py`,展示所有核心功能。

4.  **打包**: 
    - 完善 `pyproject.toml`。
    - 使用 `uv build` 打包:
      ```bash
      uv build
      ```
    - 使用 `uv publish` 或 `twine` 发布:
      ```bash
      uv publish
      # 或
      twine upload dist/*
      ```

**验收标准**: 项目可以成功打包、安装,并通过所有测试。

---

## 3. Claude Code 实现指南

与 Claude Code 协作时,请遵循以下最佳实践:

1.  **分步请求**: 按照上述开发计划,一次只请求一个或几个相关函数的实现。
    - **好**: "请为 `MacOSBackend` 实现 `get_screen_size` 和 `get_mouse_position` 方法。"
    - **不好**: "请实现整个 `MacOSBackend` 类。"

2.  **提供上下文**: 每次请求都提供相关的代码上下文,如基类定义、数据结构等。
    - **示例**: "这是 `BackendBase` 的定义,请在 `MacOSBackend` 中实现 `move_mouse` 方法。"

3.  **明确要求**: 明确指出要使用的 macOS API 和库。
    - **示例**: "请使用 `Quartz Event Services` 中的 `CGEventCreateMouseEvent` 来实现鼠标移动。"

4.  **代码规范**: 要求 Claude Code 遵循以下规范:
    - **PEP 8**: 严格遵循。
    - **类型提示**: 所有函数签名和变量都必须有类型提示。
    - **Docstrings**: 为所有公共模块、类和函数编写 Google 风格的 docstrings。
    - **异步优先**: 优先实现异步方法,然后包装成同步方法。

5.  **迭代优化**: 对 Claude Code 生成的代码进行审查,并提出修改意见。
    - **示例**: "这段代码很好,但请将 `pyobjc` 的导入放在一个私有方法 `_load_quartz` 中,实现懒加载。"

6.  **处理复杂性**: 对于复杂的实现 (如 `take_screenshot` 中的图像格式转换),可以要求 Claude Code 先提供伪代码或分步解释,然后再生成代码。

**通过这种结构化的协作方式,您可以高效地指导 Claude Code 完成整个 AutoGUI-X 项目的开发。**
