[![Docs_Onlie](https://img.shields.io/badge/在线阅读-FFAA00?logo=readthedocs&logoColor=fff)](https://isla23.github.io/300dzzCS/)

# MaaGF1 文档仓库

本Readme用于讲述如何编写、组织docs相关文档，以及其他相关事项。

## 一、编写文档

文档首先需要放入`docs/`子文件夹中，例如`FAQ.md`的路径如下：

```sh
# 相对路径
docs/tutorial/FAQ.md
# 完整路径
/home/Morning/_Workspace_/docs/docs/tutorial/FAQ.md
```

在完成文档的编写后，需要在`mkdocs.yml`的`nav:`章节添加索引，其支持多级目录，例如：

```yml
nav:
  - 首页: index.md
  - 常见问题: tutorial/FAQ.md
  - 基础教程:
    - 模拟器设置: advanced/01_virtual_monitor.md
    - 飞行棋: tutorial/base/chess/luffberry_chess.md
```

其中第一级对应的是`top bar`，第二级对应的是`left bar`；`right bar`留给文章本身的目录进行分级。

**注意**：这里的目录默认包含了`docs`前缀，因此无需在`mkdocs.yml`中添加。以`FAQ.md`为例：

```sh
# 工程目录
docs/tutorial/FAQ.md
# mkdocs.yml中编写
tutorial/FAQ.md
```

## 二、发布

仓库使用`deploy.yml`进行自动化发布，当`main`分支有改变时，自动将文档页面刷新到github.io页面。

> 需要等待2-5分支的缓存刷新时间。