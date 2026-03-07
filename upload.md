# 使用 PDM 构建和发布 optfunc2

## 前置准备

### 1. 安装 PDM
```bash
pip install pdm
```

### 2. 配置 PyPI 凭证
```bash
# 配置 PyPI 令牌（推荐使用令牌而非密码）
pdm config pypi.username __token__
pdm config pypi.password YOUR_PYPI_API_TOKEN

# 或者配置 TestPyPI（用于测试）
pdm config pypi.test_url https://test.pypi.org/simple/
pdm config pypi.test_username __token__
pdm config pypi.test_password YOUR_TESTPYPI_TOKEN
```

## 构建项目

### 1. 安装构建依赖
```bash
pdm install
```

### 2. 运行测试（可选但推荐）
```bash
# 运行所有测试
pdm run pytest

# 或运行特定测试文件
pdm run pytest src/test_optfunc2.py
```

### 3. 构建分发包
```bash
# 构建 wheel 和 source distribution
pdm build

# 构建完成后会在 dist/ 目录下生成：
# - optfunc2-0.2.7-py3-none-any.whl
# - optfunc2-0.2.7.tar.gz
```

### 4. 验证构建（可选）
```bash
# 检查构建产物
ls -lh dist/

# 验证 wheel 文件
pdm run pip install dist/optfunc2-*.whl
```

## 发布项目

### 1. 发布到 TestPyPI（推荐先测试）
```bash
# 发布到 TestPyPI
pdm publish --repository test

# 测试安装
pip install --index-url https://test.pypi.org/simple/ optfunc2
```

### 2. 发布到 PyPI
```bash
# 正式发布到 PyPI
pdm publish

# 或使用自定义 repository
pdm publish --repository pypi
```

### 3. 验证发布
```bash
# 从 PyPI 安装验证
pip install optfunc2==0.2.7

# 检查版本
pip show optfunc2
```

## 完整发布流程示例

```bash
# 1. 确保代码已提交并打标签
git add .
git commit -m "Release version 0.2.7"
git tag v0.2.7
git push && git push --tags

# 2. 安装依赖
pdm install

# 3. 运行测试
pdm run pytest

# 4. 构建项目
pdm build

# 5. 发布到 PyPI
pdm publish

# 6. 验证安装
pip install --upgrade optfunc2
```

## 常见问题

### Q: 发布时提示认证失败？
A: 确保已正确配置 PyPI API token，不要使用账号密码。在 PyPI 官网生成 API token 后使用：
```bash
pdm config pypi.password YOUR_TOKEN
```

### Q: 版本号冲突？
A: 每次发布前确保在 `pyproject.toml` 中更新版本号。

### Q: 如何跳过测试直接构建？
A: 虽然不推荐，但可以：
```bash
pdm build --no-sdist  # 只构建 wheel
```

### Q: 清理构建缓存？
```bash
rm -rf dist/ build/ *.egg-info
```

## 注意事项

1. **版本号管理**: 每次发布前在 `pyproject.toml` 中更新 [project] 版本的 version 字段
2. **CHANGELOG**: 建议在 README.md 或单独的文件中记录版本变更
3. **测试先行**: 强烈建议先发布到 TestPyPI 测试无误后再发布到正式 PyPI
4. **Git 标签**: 为每个发布版本创建 Git tag 便于版本追踪
5. **Python 版本兼容性**: 确保 `requires-python` 配置正确（当前为 >=3.8,<4.0）
