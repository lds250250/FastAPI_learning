# FastAPI 学习路线与进度追踪

## 第 0 周：环境准备与工具链打通（已完成）
- **Day 1**：安装 Python 3.10+、Git、VS Code 及必备插件，配置 GitHub Copilot。
- **Day 2**：配置 GitHub 账号，生成并配置 SSH 密钥，理解公钥与私钥的安全机制。
- **Day 3**：安装 `uv` 包管理器，解决环境变量问题，使用 `uv sync` 同步环境并成功跑通 FastAPI 的 Hello World。

## 第一阶段：FastAPI 核心基础与 Pydantic 数据校验（第 1 周）
- **Day 1**：路径参数与查询参数（Path & Query Params）。
- **Day 2**：Pydantic 请求体与数据模型（BaseModel）。
- **Day 3**：Pydantic 进阶校验（Field & Validators，包括 `...` 和 `| None` 的用法）。
- **Day 4**：响应模型（Response Model）与出口把关。
- **Day 5**：状态码（Status Codes）与 RESTful 规范。
- **Day 6**：接口进阶与文档规范（Tags、Summary、HTTPException 主动抛错机制）。
- **Day 7**：第一周实战任务（开发一个包含增删改查的极简工具接口项目，巩固本周所有知识点）。

## 第二阶段：核心特性与架构拆分（第 2 周）
- **Day 1**：Pydantic V2 核心配置与模型规范（`model_config`）。
- **Day 2**：高级字段校验（`field_validator` 与 `model_validator`）。
- **Day 3**：响应模型进阶与序列化控制（`exclude` 与 `alias`）。
- **Day 4**：`Annotated` 注解与自定义类型、`TypeAdapter`。
- **Day 5**：请求模型与响应模型分离（Create / Read / Update 架构）。
- **Day 6**：第二周综合实战（极简图书管理系统 CRUD）。

## 第二阶段：核心特性与架构拆分（第 3 周）
- **Day 1**：用户注册模型与嵌套校验（`EmailStr`、嵌套 Profile 模型）。
- **Day 2**：密码处理与敏感字段过滤（模拟哈希、`exclude=True`）。
- **Day 3**：用户登录逻辑与错误处理（`fake_users_db`、`HTTPException`）。
- **Day 4**：综合实战（上）—— 完善用户 CRUD 与密码安全更新。
- **Day 5**：综合实战（下）—— 代码重构、`Annotated` 优化与模板化。

## 第三阶段：架构拆分与依赖注入（第 4 周）
- 采用分层架构（路由层、业务层、数据层等），使用 `APIRouter` 进行路由拆分与模块化管理，通过 `pydantic-settings` 管理环境变量。

## 第三阶段：架构拆分与依赖注入（第 5 周）
- 掌握全局/路由/单接口依赖注入（`Depends`），实现依赖复用、嵌套依赖及参数封装，基于依赖实现限流、日志记录及权限拦截。

## 第三阶段：架构拆分与依赖注入（第 6 周）
- 理解 OAuth2 协议核心流程，实现 JWT 令牌生成、校验、过期刷新及密码哈希加密，建立基于角色的权限控制体系。

## 第四阶段：异步数据库与高级特性（第 7 周）
- 使用 SQLAlchemy 2.0 异步模式及会话管理，掌握 MySQL/PostgreSQL 异步 CRUD 全流程，使用 Alembic 进行数据库迁移。

## 第四阶段：异步数据库与高级特性（第 8 周）
- 掌握 WebSocket 实时连接与消息收发，集成 Redis 异步缓存，实现接口限流、防刷策略，封装查询分页、排序、筛选通用逻辑。

## 第五阶段：部署运维与架构拔高（第 9 周）
- 使用 TestClient 进行单元测试，编写 pytest 测试用例；实施日志分级、持久化及错误上报，使用 Lifespan 管理启动/关闭钩子函数。

## 第五阶段：部署运维与架构拔高（第 10 周）
- 掌握 Docker 容器化部署、Docker Compose 编排、Nginx 反向代理及 Gunicorn 进程守护；理解微服务拆分思路，优化异步 IO，适配高并发场景。

