给rime生成用于双拼(小鹤双拼)的拆字字典，以uu为起始，再输入拆字内容，如：

“犇”字为uu nq nq nq；



使用方法：
1. 运行python3 chaizi.py生成double_pinyin_flypy.chaizi.dict.yaml，或直接下载double_pinyin_flypy.chaizi.dict.yaml文件；
2. 将double_pinyin_flypy.chaizi.dict.yaml文件放入rime的用户目录；
3. 在自定义字典中加入double_pinyin_flypy.chaizi；
4. 重新部署；
5. enjoy；



依赖：

- pypinyin



代码内容参考：
1. https://github.com/bcaso/pinyin_to_double_pinyin.git
2. https://github.com/taishan1994/stroke2vec.git
3. http://gerry.lamost.org/blog/?p=296003
