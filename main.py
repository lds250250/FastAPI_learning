from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field
from fastapi import status
from fastapi import HTTPException

app = FastAPI()

"""🎯 1.7 实战任务：构建一个“班级管理系统”
1. 业务需求
我们需要开发一个接口，用于创建一个班级。这个班级不仅有基本信息，还包含多名学生。
2. 你需要完成的任务
定义 Student 模型：
包含字段：name（姓名，字符串）、age（年龄，整数）。
加上合理的校验（比如年龄必须大于 0）。
定义 ClassroomCreate 模型：
包含字段：class_name（班级名称，字符串）。
包含字段：students（学生列表，这里需要用到 Python 的 list 类型）。
编写 POST 接口：
路径：/classrooms/
接收 ClassroomCreate 对象。
成功创建后，返回 201 状态码，并返回班级名称以及该班级的学生人数。
3. 你的学习参考资料
官方文档指引：请去 FastAPI 官方文档搜索 “Body - Nested Models”（请求体 - 嵌套模型）这一节。里面详细讲解了如何在 Pydantic 中定义包含列表（list）的模型。
Python 基础提示：在 Python 中，表示一个包含多个对象的列表，类型提示通常写成 list[Student]。
🚀 你的行动指南
打开你的 main.py。
查阅官方文档，思考 list[Student] 该怎么用。
动手敲代码，完成接口。
遇到任何报错或卡壳，随时问我！
写完后，直接把完整的 main.py 代码发给我，我来给你做专业的 Code Review。"""

