# My Blog

这是我的个人博客，使用 Python 静态博客生成器构建。

## 特性

- 支持 Markdown 写作
- 自动代码高亮
- 响应式设计
- 支持明暗主题切换
- 标签分类

## 项目结构

```
blog/
├── templates/          # 模板文件
├── styles/            # CSS 样式文件
├── posts/             # Markdown 文章
├── public/            # 生成的静态文件
└── static_blog_generator.py  # 生成器脚本
```

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

## 部署流程

### 首次部署

1. 确保已安装 Git 并配置 SSH 密钥
```bash
git config --global user.name "shisuiyi"
git config --global user.email "你的邮箱"
```

2. 初始化仓库
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin git@github.com:shisuiyi/shisuiyi.github.io.git
git push -u origin main
```

3. 给部署脚本添加执行权限
```bash
chmod +x deploy.sh
```

4. 执行部署
```bash
./deploy.sh
```

### 日常更新

1. 更新博客内容后，提交源代码到 blog-source 仓库：
```bash
git add .
git commit -m "更新说明"
git push origin main
```

2. 部署到 GitHub Pages：
```bash
./deploy.sh
```

## 写作指南

1. 在 `blog/posts/` 目录下创建 `.md` 文件
2. 文件开头添加 YAML 格式的元数据：
```yaml
---
title: 文章标题
date: YYYY-MM-DD
tags: [标签1, 标签2]
---
```
3. 使用 Markdown 语法编写文章内容
4. 执行 `./deploy.sh` 部署更新

## 自动部署

本项目配置了 GitHub Actions，当推送到 main 分支时会自动部署。
配置文件位于 `.github/workflows/deploy.yml`。

## 文件说明

- `deploy.sh`: 部署脚本
- `.gitignore`: Git 忽略文件配置
- `blog/templates/`: 网站模板
- `blog/styles/`: 样式文件
- `blog/posts/`: 博客文章
- `.github/workflows/`: GitHub Actions 配置

## 许可证

MIT 