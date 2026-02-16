# AutoGUI-X 开发文档

本目录包含 AutoGUI-X 项目的完整开发文档,适合使用 Claude Code 或其他 AI 辅助工具进行实现。

---

## 📚 文档清单

### 1. [系统设计文档](./AutoGUIX_System_Design.md)

**用途**: 了解项目架构和技术方案

**内容**:
- 三层插件化架构设计
- 核心数据结构定义
- `BackendBase` 抽象基类完整接口
- 项目文件结构
- 依赖管理方案 (使用 uv)

**适合**: 在开始编码前阅读,理解整体架构

---

### 2. [开发计划文档](./AutoGUIX_Development_Plan.md)

**用途**: 按步骤实现项目功能

**内容**:
- 开发环境设置指南
- 五个开发阶段 (每个阶段 1-4 小时)
- 每个阶段的详细任务和验收标准
- Claude Code 协作最佳实践

**适合**: 实际开发时作为任务清单使用

---

### 3. [Claude Code 协作指南](./AutoGUIX_Claude_Code_Guide.md)

**用途**: 使用 Claude Code 高效开发

**内容**:
- 每个阶段的详细提示词模板 (可直接复制粘贴)
- 代码审查清单
- 常见问题和解决方案
- 测试和验证脚本

**适合**: 使用 Claude Code 时参考,提高开发效率

---

### 4. [uv 使用指南](./UV_Migration_Guide.md)

**用途**: 了解 uv 包管理工具

**内容**:
- uv 简介和优势
- Poetry vs uv 命令对比
- pyproject.toml 配置示例
- 完整的开发工作流
- 常用命令参考

**适合**: 不熟悉 uv 的开发者

---

## 🚀 快速开始

### 第一步: 阅读系统设计

```bash
# 阅读系统设计文档,理解架构
cat docs/AutoGUIX_System_Design.md
```

### 第二步: 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/VoyagerTechHQ/autoguix.git
cd autoguix

# 创建虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖
uv pip install -e ".[locate,dev]"
```

### 第三步: 开始开发

按照 `AutoGUIX_Development_Plan.md` 中的五个阶段逐步实现:

1. **阶段一**: 核心数据类型 (1-2 小时)
2. **阶段二**: 抽象基类 (1-2 小时)
3. **阶段三**: macOS 后端 (3-4 小时)
4. **阶段四**: 核心管理器 (2-3 小时)
5. **阶段五**: 用户 API (3-4 小时)

### 第四步: 使用 Claude Code

如果使用 Claude Code,参考 `AutoGUIX_Claude_Code_Guide.md` 中的提示词模板:

```
请为 AutoGUI-X 项目实现核心数据类型。

文件: autoguix/core/types.py

要求:
1. 使用 typing.NamedTuple 定义以下类:
   - Point: x (int), y (int)
   - Size: width (int), height (int)
   - Region: left (int), top (int), width (int), height (int)
...
```

---

## 📊 预计时间

- **总开发时间**: 11-16 小时
- **阶段一**: 1-2 小时
- **阶段二**: 1-2 小时
- **阶段三**: 3-4 小时
- **阶段四**: 2-3 小时
- **阶段五**: 3-4 小时
- **测试和调试**: 1-2 小时

---

## ✅ 验收标准

完成开发后,确保:

- [ ] 所有核心 API 已实现
- [ ] 单元测试覆盖率 > 80%
- [ ] 代码格式检查通过 (black, ruff)
- [ ] 文档字符串完整 (Google 风格)
- [ ] 示例代码可运行
- [ ] 与 PyAutoGUI API 100% 兼容

---

## 🤝 贡献

如果您在使用这些文档时发现问题或有改进建议,欢迎:

- 提交 Issue: https://github.com/VoyagerTechHQ/autoguix/issues
- 提交 Pull Request
- 参与 Discussions (如果已启用)

---

## 📄 许可证

这些文档与 AutoGUI-X 项目使用相同的 BSD-3-Clause 许可证。

---

**祝开发顺利！** 🚀🍎
