# AutoGUI-X - uv 包管理工具迁移指南

**版本**: 1.0  
**日期**: 2026年2月16日

---

## 📦 为什么选择 uv?

**uv** 是由 Astral (Ruff 的创建者) 开发的新一代 Python 包管理工具,使用 Rust 编写,具有以下优势:

1. **极快的速度**: 比 pip 快 10-100 倍,比 Poetry 快 10-20 倍
2. **现代化**: 原生支持 PEP 621 (pyproject.toml 标准)
3. **兼容性**: 完全兼容 pip,可以无缝替换
4. **简洁**: 命令简单直观,学习曲线平缓
5. **活跃维护**: 由 Astral 团队积极维护

---

## 🚀 快速开始

### 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv

# 验证安装
uv --version
```

### 基本命令对比

| 操作 | Poetry | uv |
|------|--------|-----|
| 创建项目 | `poetry new project` | `mkdir project && cd project && uv init` |
| 安装依赖 | `poetry install` | `uv pip install -e .` |
| 添加依赖 | `poetry add package` | 编辑 `pyproject.toml` 后运行 `uv pip install -e .` |
| 运行脚本 | `poetry run python script.py` | `python script.py` (在激活的虚拟环境中) |
| 构建包 | `poetry build` | `uv build` |
| 发布包 | `poetry publish` | `uv publish` 或 `twine upload dist/*` |

---

## 📝 pyproject.toml 配置

### Poetry 风格 (旧)

```toml
[tool.poetry]
name = "autoguix"
version = "0.1.0"
description = "..."

[tool.poetry.dependencies]
python = "^3.8"
Pillow = "^10.0.0"
```

### PEP 621 标准 (新 - uv 推荐)

```toml
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

## 🔧 AutoGUI-X 开发工作流

### 1. 初始化项目

```bash
mkdir autoguix
cd autoguix
uv init
```

### 2. 创建 pyproject.toml

使用系统设计文档中提供的配置。

### 3. 创建虚拟环境 (可选但推荐)

```bash
uv venv
source .venv/bin/activate  # macOS/Linux
```

### 4. 安装依赖

```bash
# 安装核心依赖
uv pip install -e .

# 安装可选依赖 (图像定位)
uv pip install -e ".[locate]"
```

### 5. 开发和测试

```bash
# 运行测试
pytest

# 运行示例
python examples/macos_demo.py
```

### 6. 构建和发布

```bash
# 构建
uv build

# 发布到 PyPI
uv publish
# 或
twine upload dist/*
```

---

## 💡 常用命令

### 依赖管理

```bash
# 安装项目 (可编辑模式)
uv pip install -e .

# 安装特定包
uv pip install package-name

# 安装特定版本
uv pip install "package-name>=1.0.0"

# 卸载包
uv pip uninstall package-name

# 列出已安装的包
uv pip list

# 导出依赖
uv pip freeze > requirements.txt
```

### 虚拟环境

```bash
# 创建虚拟环境
uv venv

# 创建指定 Python 版本的虚拟环境
uv venv --python 3.11

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 构建和发布

```bash
# 构建 wheel 和 sdist
uv build

# 发布到 PyPI
uv publish

# 发布到 Test PyPI
uv publish --repository testpypi
```

---

## 🔄 从 Poetry 迁移

如果您之前使用 Poetry,可以按照以下步骤迁移:

### 1. 转换 pyproject.toml

将 `[tool.poetry]` 部分转换为 `[project]` 部分 (参考上面的示例)。

### 2. 删除 Poetry 相关文件

```bash
rm poetry.lock
rm -rf .venv  # 如果使用 Poetry 的虚拟环境
```

### 3. 使用 uv 重新安装

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

### 4. 更新 CI/CD 配置

将 CI/CD 脚本中的 `poetry install` 替换为 `uv pip install -e .`。

---

## 📚 更多资源

- **uv 官方文档**: https://github.com/astral-sh/uv
- **PEP 621 规范**: https://peps.python.org/pep-0621/
- **Hatchling 文档**: https://hatch.pypa.io/latest/

---

## ✅ 总结

使用 uv 作为 AutoGUI-X 的包管理工具,您将获得:

- ✅ **更快的安装速度** (10-100x)
- ✅ **更简洁的配置** (标准 PEP 621)
- ✅ **更好的兼容性** (完全兼容 pip)
- ✅ **更现代的工具链**

**所有文档已更新为使用 uv。开始您的 AutoGUI-X 开发之旅吧！** 🚀
