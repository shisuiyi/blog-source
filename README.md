# My Blog

这是我的个人博客，使用 Python 静态博客生成器构建。

## 特性

- 支持 Markdown 写作
- 自动代码高亮
- 响应式设计
- 支持明暗主题切换
- 标签分类

## 本地开发

1. 克隆仓库
```bash
git clone git@github.com:shisuiyi/shisuiyi.github.io.git
cd shisuiyi.github.io
```

2. 安装依赖
```bash
pip install pyyaml markdown pygments
```

3. 生成静态文件
```bash
python blog/static_blog_generator.py
```

4. 部署
```bash
./deploy.sh
```

## 许可证

MIT 