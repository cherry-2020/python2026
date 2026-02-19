# PostgreSQL聊天内容保存工具

本项目提供了一个简单易用的工具，帮助您将聊天内容保存到PostgreSQL数据库中。

## 项目概述

本项目包含以下几个主要文件：

- `chat_to_db.py` - 核心模块，包含`ChatDatabase`类，实现与PostgreSQL数据库的交互功能
- `聊天内容保存到数据库指南.md` - 详细的使用指南和文档
- `set_db_env.bat` - Windows批处理文件，帮助设置数据库连接环境变量
- `db_config_gui.py` - 图形界面的数据库配置工具
- `db_test.py` - 数据库连接测试脚本

## 功能特点

- 支持将聊天消息保存到PostgreSQL数据库
- 提供多种数据库连接方式（直接修改代码、环境变量、GUI配置）
- 支持按发送者查询消息
- 支持按关键词搜索消息
- 提供详细的错误处理和日志输出
- 支持上下文管理器（with语句）自动管理连接
- 包含图形界面配置工具，方便非技术用户使用

## 快速开始

### 1. 安装必要的依赖

```bash
pip install psycopg2-binary
```

### 2. 配置数据库连接

您可以通过以下三种方式之一配置数据库连接：

#### 方式1：直接修改代码

打开`chat_to_db.py`文件，修改默认的数据库连接信息：

```python
self.db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:123456@localhost:5432/mydb')
```

#### 方式2：使用环境变量

运行`set_db_env.bat`批处理文件，按照提示设置环境变量：

```cmd
set_db_env.bat
```

#### 方式3：使用图形界面配置工具

运行`db_config_gui.py`启动图形界面配置工具：

```cmd
python db_config_gui.py
```

在界面中填写数据库连接信息，点击"生成连接字符串"，然后点击"设置环境变量"。

### 3. 在您的应用中使用

```python
from chat_to_db import ChatDatabase

# 方法1：基本用法
chat_db = ChatDatabase()
if chat_db.connect():
    # 保存聊天消息
    chat_db.save_chat("用户1", "你好，这是一条测试消息")
    
    # 获取聊天消息
    chats = chat_db.get_chats()
    for chat in chats:
        print(f"[{chat[2]}] {chat[0]}: {chat[1]}")
    
    # 关闭连接
    chat_db.close()

# 方法2：使用上下文管理器（推荐）
try:
    with ChatDatabase() as chat_db:
        # 保存聊天消息
        chat_db.save_chat("用户2", "这是使用上下文管理器保存的消息")
        
        # 搜索消息
        search_results = chat_db.search_chats("测试")
        for chat in search_results:
            print(f"[{chat[2]}] {chat[0]}: {chat[1]}")
except Exception as e:
    print(f"操作数据库时出错: {e}")
```

## 数据库表结构

程序会自动创建名为`chat_messages`的表（如果不存在），表结构如下：

```sql
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 常见问题解决

### 1. 连接数据库失败

- 确保PostgreSQL服务已启动
- 检查数据库连接信息是否正确
- 确保您的用户有权限访问数据库
- 检查防火墙是否允许连接到PostgreSQL端口

### 2. 编码错误

如果遇到编码错误，请尝试以下方法：
- 在数据库URL中避免使用中文或特殊字符
- 使用图形界面配置工具生成正确的连接字符串
- 确保环境变量设置正确

### 3. 其他问题

如果遇到其他问题，请参考`聊天内容保存到数据库指南.md`文件获取详细的解决方案。

## 扩展建议

根据您的实际需求，您可以扩展这个工具：

- 添加用户认证功能
- 支持更多消息类型（文本、图片、文件等）
- 实现聊天会话管理
- 添加消息加密功能
- 实现分页查询大量历史消息

## 关于

本工具设计用于帮助开发者快速实现聊天内容的数据库存储功能。如果您有任何问题或建议，欢迎提出。