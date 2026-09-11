# FastAPI 学习路线与进度追踪

## 第 0 周：环境准备与工具链打通（已完成）（已完成）
- **Day 1**：安装 Python 3.10+、Git、VS Code 及必备插件，配置 GitHub Copilot。
- **Day 2**：配置 GitHub 账号，生成并配置 SSH 密钥，理解公钥与私钥的安全机制。
- **Day 3**：安装 `uv` 包管理器，解决环境变量问题，使用 `uv sync` 同步环境并成功跑通 FastAPI 的 Hello World。

## 第一阶段：FastAPI 核心基础与 Pydantic 数据校验（第 1 周）（已完成）
- **Day 1**：路径参数与查询参数（Path & Query Params）。
- **Day 2**：Pydantic 请求体与数据模型（BaseModel）。
- **Day 3**：Pydantic 进阶校验（Field & Validators，包括 `...` 和 `| None` 的用法）。
- **Day 4**：响应模型（Response Model）与出口把关。
- **Day 5**：状态码（Status Codes）与 RESTful 规范。
- **Day 6**：接口进阶与文档规范（Tags、Summary、HTTPException 主动抛错机制）。
- **Day 7**：第一周实战任务（开发一个包含增删改查的极简工具接口项目，巩固本周所有知识点）。

## 第二阶段：核心特性与架构拆分（第 2 周）（已完成）
- **Day 1**：Pydantic V2 核心配置与模型规范（`model_config`）。
- **Day 2**：高级字段校验（`field_validator` 与 `model_validator`）。
- **Day 3**：响应模型进阶与序列化控制（`exclude` 与 `alias`）。
- **Day 4**：`Annotated` 注解与自定义类型、`TypeAdapter`。
- **Day 5**：请求模型与响应模型分离（Create / Read / Update 架构）。
- **Day 6**：第二周综合实战（极简图书管理系统 CRUD）。

## 第二阶段：核心特性与架构拆分（第 3 周）（已完成）
- **Day 1**：用户注册模型与嵌套校验（`EmailStr`、嵌套 Profile 模型）。
- **Day 2**：密码处理与敏感字段过滤（模拟哈希、`exclude=True`）。
- **Day 3**：用户登录逻辑与错误处理（`fake_users_db`、`HTTPException`）。
- **Day 4**：综合实战（上）—— 完善用户 CRUD 与密码安全更新。
- **Day 5**：综合实战（下）—— 代码重构、`Annotated` 优化与模板化。

## 第三阶段：架构拆分与依赖注入（第 4 周）（已完成）
- **Day 1**：环境变量管理与配置解耦（`pydantic-settings`、`.env` 文件与 `Settings` 单例）。
- **Day 2**：分层架构设计与目录重构（四层职责划分、依赖方向与 `src-layout` 目录树）。
- **Day 3**：数据层封装（把 `fake_users_db` 抽成 `Repository`，数据层不碰 HTTP）。
- **Day 4**：业务层封装（把密码哈希与业务规则抽成 `Service`）。
- **Day 5**：路由层瘦身与 `APIRouter` 模块化组装（`prefix`、`tags` 与多模块注册）。
- **Day 6**：各层串联与依赖落地（`deps.py` 提供 `repo` / `service` / `current_user` 依赖）。
- **Day 7**：第四周综合实战（上）—— 按分层架构新增一个业务模块，独立完成 CRUD。
- **Day 8**：第四周综合实战（下）—— 全接口兼容性验证、补充 `.env.example`、更新 README 与架构笔记。

## 第三阶段：架构拆分与依赖注入（第 5 周）（已完成）
- **Day 1**：类作为依赖（`__init__` 声明参数、`__call__` 返回，把一组查询参数封装成对象）。
- **Day 2**：依赖的解析机制（全局 / 路由级 / 单接口级作用域，与请求级缓存 `use_cache`）。
- **Day 3**：带清理的依赖（`yield` 依赖与资源管理，为数据库会话铺路）。
- **Day 4**：权限拦截依赖（读取 `Header`、401 与 403 语义、角色校验依赖）。
- **Day 5**：限流与请求日志依赖（内存计数器限流、429、请求耗时统计）。
- **Day 6**：第五周综合实战 —— 给用户与图书模块接入分页、权限、限流依赖，并更新 README。

## 第三阶段：架构拆分与依赖注入（第 6 周）
- **Day 1**：中间件基础（CORS 跨域、自定义中间件）。
- **Day 2**：请求日志中间件与「依赖 vs 中间件」的分工边界。
- **Day 3**：全局异常处理器（统一错误响应格式）。
- **Day 4**：自定义业务异常体系（Service 抛业务异常，由处理器统一翻译成 HTTP）。
- **Day 5**：第六周综合实战 —— 给现有模块接入中间件与统一异常处理，并更新 README。

## 第四阶段：测试、认证与异步数据库（第 7 周）
- **Day 1**：`pytest` 入门与测试目录组织（命名规范、断言、运行方式）。
- **Day 2**：`fixture` —— 测试世界的「依赖注入」。
- **Day 3**：`TestClient` 接口测试（状态码与响应体断言）。
- **Day 4**：`dependency_overrides`（测试时把真实依赖替换成假实现）。
- **Day 5**：分层测试（脱离 HTTP 单测 Service 与 Repository，理解「测行为，不测实现」）。
- **Day 6**：第七周综合实战 —— 给用户与图书模块补齐测试，并更新 README。

## 第四阶段：测试、认证与异步数据库（第 8 周）
- **Day 1**：密码哈希（`passlib` + `bcrypt`，替换第 3 周的假哈希）。
- **Day 2**：OAuth2 密码流与 `/token` 表单接口（`OAuth2PasswordRequestForm`）。
- **Day 3**：JWT 结构与令牌生成（`SECRET_KEY`、`ALGORITHM` 终于派上用场）。
- **Day 4**：令牌校验与 `get_current_user` 改造（从路径参数改为读请求头）。
- **Day 5**：令牌过期与刷新（`exp` 声明与刷新思路）。
- **Day 6**：基于角色的权限控制（RBAC，与第 5 周的角色依赖合流）。
- **Day 7**：第八周综合实战 —— 完成登录闭环并保护现有接口，更新 README。

## 第四阶段：测试、认证与异步数据库（第 9 周）
- **Day 1**：同步、并发、异步各自在解决什么问题。
- **Day 2**：事件循环与 `await` 的本质。
- **Day 3**：假异步 —— 在 `async def` 里写阻塞代码的代价。
- **Day 4**：并发编排（`asyncio.gather` 与任务）。
- **Day 5**：第九周综合实战 —— 对比串行 / 并发 / 假异步三种写法的耗时。

## 第四阶段：测试、认证与异步数据库（第 10 周）
- **Day 1**：异步数据库引擎与连接配置（`create_async_engine`、`DATABASE_URL`）。
- **Day 2**：连接与会话管理（`async_sessionmaker` 与第 5 周学的 `yield` 依赖）。
- **Day 3**：SQLAlchemy 2.0 ORM 模型（`DeclarativeBase`、`Mapped`、`mapped_column`）。
- **Day 4**：建表与初始化数据（`create_all` 与种子数据）。
- **Day 5**：第十周综合实战 —— 打通「引擎 + 会话 + 模型」，能连上真实数据库。

## 第四阶段：测试、认证与异步数据库（第 11 周）
- **Day 1**：Repository 改造（把内存字典换成真实 SQL CRUD，Service 层不动）。
- **Day 2**：表关系与外键（一对多建模、`relationship`）。
- **Day 3**：Alembic 迁移入门（初始化、生成迁移文件）。
- **Day 4**：迁移的升级、回滚与版本管理。
- **Day 5**：分页、排序、筛选的通用封装（把第 5 周的依赖升级为可复用组件）。
- **Day 6**：第十一周综合实战 —— 全模块接入数据库，并验证第 7 周写的测试仍然存活。

## 第五阶段：缓存、实时通信与可观测性（第 12 周）
- **Day 1**：Redis 连接与异步客户端（`redis.asyncio`、连接配置进 `.env`）。
- **Day 2**：缓存模式（读缓存、缓存失效、缓存穿透的基本应对）。
- **Day 3**：把内存限流升级为 Redis 限流（多进程 / 多实例共享计数）。
- **Day 4**：防刷与滑动窗口（更精确的限流算法）。
- **Day 5**：第十二周综合实战 —— 给图书模块接入缓存与分布式限流，并更新 README。

## 第五阶段：缓存、实时通信与可观测性（第 13 周）
- **Day 1**：WebSocket 基础与握手（与 HTTP 的差异、`/ws` 端点）。
- **Day 2**：连接管理器（登记连接、管理在线用户）。
- **Day 3**：消息收发与广播（单播、群发、`WebSocketDisconnect`）。
- **Day 4**：WebSocket 鉴权（复用第 8 周的 JWT 依赖）。
- **Day 5**：第十三周综合实战 —— 实现一个实时通知端点，并更新 README。

## 第五阶段：缓存、实时通信与可观测性（第 14 周）
- **Day 1**：`logging` 模块与日志分级（DEBUG / INFO / WARNING / ERROR）。
- **Day 2**：日志格式化与持久化（写入文件、按天切割）。
- **Day 3**：请求级上下文（Request ID 贯穿一次请求的所有日志）。
- **Day 4**：错误上报与堆栈记录（与第 6 周的异常处理器合流）。
- **Day 5**：`Lifespan` 启动 / 关闭钩子（连接池初始化与优雅关闭）。
- **Day 6**：第十四周综合实战 —— 全项目接入统一日志，并更新 README。

## 第六阶段：部署运维与性能调优（第 15 周）
- **Day 1**：Dockerfile —— 把应用打包成镜像（基础镜像、依赖安装、启动命令）。
- **Day 2**：多阶段构建与镜像瘦身（分层缓存、`.dockerignore`）。
- **Day 3**：Docker Compose 编排（应用 + 数据库 + Redis 一键启动）。
- **Day 4**：Nginx 反向代理与 Gunicorn + Uvicorn 进程模型。
- **Day 5**：第十五周综合实战 —— 用 Compose 完整部署一套环境，并更新 README。

## 第六阶段：部署运维与性能调优（第 16 周）
- **Day 1**：数据库连接池配置与调优。
- **Day 2**：异步 IO 与并发瓶颈定位。
- **Day 3**：压测入门（给接口打流量、观察关键指标）。
- **Day 4**：缓存与限流在高并发下的调优。
- **Day 5**：第十六周综合实战 —— 出一份压测与调优报告，并更新 README。

