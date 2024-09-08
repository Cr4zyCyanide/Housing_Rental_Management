*完成于2024-05-22* 

*暂停维护*

个人于2024年5月完成的Web程序开发课程设计，前端采用Vue3+TypeScript+Element-Plus，后端采用Flask框架，数据库使用MySQL。

## 开发环境

- [VS Code](https://code.visualstudio.com/) + [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (previously Volar) and disable Vetur + python3.12
- PyCharm Professional

## 运行和构建

```shell
# pnpm
pnpm install
pnpm run dev
# build
pnpm build
# back-end
cd flask
python app.py
```

运行后输出的文件保存在该目录下的dist文件夹内
默认后端接口地址在127.0.0.1:4567

如果需数据进行测试可运行data_generator.py，初始化数据库可使用sql.py中createDatabase方法和createTable方法。
