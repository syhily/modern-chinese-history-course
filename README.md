# 中国近现代史（Modern and Contemporary History of China）

章开沅、朱英 主编 · 河南大学出版社 · 2009 年 8 月第 1 版（ISBN 978-7-81091-939-5）

本项目将扫描版《中国近现代史》排版为 EPUB 3 电子书。正文文字由 [MinerU](https://github.com/opendatalab/MinerU) 双模式（pipeline / vlm）识别：pipeline 结果无幻觉、作为校对底稿，vlm 结果用于复杂版式交叉比对；原书的页底圈码脚注（①②③，每页重新编号）逐页对照扫描原页补回并转为随文弹注。中间稿为 Markdown，由 pandoc 构建。

全书十三章：前近代时期的中国社会（1500～1840）／近代中国社会的开始／新社会结构的发生／民族危机的加深／民族运动的递进／清末新政和辛亥革命／社会与文化的新变化／民初的政治与社会／社会转折的新取向／南京国民政府初期的内政外交／苏维埃革命的兴起与受挫／抗日战争／历史的新转折，书末附后记。每章含本章小结、学术综述、参考书目、思考题四个栏目。

## 文件结构

| 文件 | 说明 |
| --- | --- |
| `manuscript/00-frontmatter.md` | 前置部分（电子版说明、书名页、版权信息） |
| `manuscript/chNN.md` | 十三章正文（**所有修改都在对应文件里进行**），构建时按文件名序合并 |
| `manuscript/14-postscript.md` | 后记（含各章作者及单位名单） |
| `metadata.yaml` | pandoc 元数据（书名、编者、出版社、ISBN） |
| `assets/epub.css` | EPUB 样式（正文用阅读器默认字体；标题黑体 / 引文楷体 / 扉页仿宋；边框表格、表题样式） |
| `assets/cover.jpg` | 封面图（以同系列《中国古代史教程》封面版式为基，按本书封面配色与文字重绘，生成脚本见 `scripts/make_cover.py`） |
| `scripts/build.sh` | pandoc 构建脚本（`--split-level=1` 按章拆分文件，章内连续排版；`\newpage` 经 Lua 过滤器转硬分页；CSS 剥注释后打包，兼容 Clearview） |
| `scripts/ocr.sh` | MinerU 双模式 OCR 脚本（100 页/片分片、断点续跑；`make ocr`） |
| `scripts/make_cover.py` | 封面生成脚本（PIL 绘制，配色采样自原书封面扫描页） |
| `scripts/newpage.lua` | pandoc Lua 过滤器：`\newpage` 转硬分页 |
| `scripts/ascii-heading-ids.lua` | pandoc Lua 过滤器：标题锚点改写为 ASCII 序号（sec-N），否则中文锚点在部分阅读器中目录无法跳转 |
| `scripts/chapter-titlepage.lua` | pandoc Lua 过滤器：「第X章」标题拆分为小字章次 + 大字章题，章扉页居中宋体 |
| `scripts/pangu.lua` | pandoc Lua 过滤器：中西文之间加间距 |
| `Makefile` | `make build` 构建，`make ocr` OCR，`make clean` 清理 |
| `docs/workflow.md` | 转换约定与校对流程的完整说明（页码换算、标题层级、脚注核对、自查命令） |
| `中国近现代史.epub` | 构建产物（不入库，见 Releases） |

原始 PDF 与 OCR 中间结果（`source/`、`ocr/`）不入库，请自行准备。

## 下载

每次打 tag 都会由 GitHub Actions 自动构建 EPUB 并发布到 Releases：

- [下载最新版 EPUB](https://github.com/syhily/modern-chinese-history-course/releases/latest/download/modern-chinese-history-course.epub)（直链，始终指向最新 Release）

## 致谢

- EPUB 样式表的字体栈来自 [fonts.css](https://github.com/zenozeng/fonts.css)（MIT License），排版规则借鉴 [typo.css](https://github.com/sofish/typo.css)（MIT License）。
- 工程项目结构沿袭同系列[《中国古代史教程》电子书项目](https://github.com/syhily/ancient-chinese-history-course)。

## 版权说明

本书著作权归原作者及河南大学出版社所有。本电子版仅供个人学习与研究使用，不进行任何商业用途。内容请以纸质原书为准。若涉及侵权，请联系仓库所有者，核实后将立即删除。
