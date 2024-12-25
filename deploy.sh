#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 确保脚本抛出遇到的错误
set -e

# 生成静态文件
echo -e "${BLUE}正在生成静态文件...${NC}"
python3 blog/static_blog_generator.py

# 进入生成的文件夹
cd blog/public

# 初始化 git 仓库（如果还没有的话）
if [ ! -d ".git" ]; then
    git init
    git checkout -b main
fi

# 添加文件到暂存区
echo -e "${BLUE}添加文件到暂存区...${NC}"
git add -A

# 提交更改
echo -e "${BLUE}提交更改...${NC}"
timestamp=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Site updated: ${timestamp}"

# 推送到 GitHub Pages 仓库
echo -e "${BLUE}推送到 GitHub...${NC}"
git push -f git@github.com:shisuiyi/shisuiyi.github.io.git main

echo -e "${GREEN}部署完成!${NC}"

cd ../.. 