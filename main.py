import json

import aiohttp
from loguru import logger
import tomllib  # 确保导入tomllib以读取配置文件
import os  # 确保导入os模块

from WechatAPI import WechatAPIClient
from utils.decorators import *
from utils.plugin_base import PluginBase


class PushMessagesPlugin(PluginBase):
    description = "推送消息到对应的地址"
    author = "milian221"
    version = "1.0.0"

    # 同步初始化
    def __init__(self):
        super().__init__()

        # 获取配置文件路径
        self.baseUri = ''
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)

            # 读取基本配置
            basic_config = config.get("basic", {})
            self.enable = basic_config.get("enable", False)  # 读取插件开关
            self.baseUri = basic_config.get("base_uri", '')  # 推送地址
            self.pushList = basic_config.get("push_list", '')  # 推送地址

        except Exception as e:
            logger.error(f"加载PushMessagesPlugin配置文件失败: {str(e)}")
            self.enable = False  # 如果加载失败，禁用插件

    # 异步初始化
    async def async_init(self):
        return

    @on_text_message(priority=50)
    async def handle_text(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return  # 如果插件未启用，直接返回
        if 'handle_text' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了文本消息。 \n{message}")
        return True

    @on_xml_message(priority=50)
    async def handle_xml(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return  # 如果插件未启用，直接返回
        if 'handle_xml' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了xml消息。 \n{message}")
        return True

    @on_at_message(priority=50)
    async def handle_at(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return
        if 'handle_at' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了被@消息。 \n{message}")

    @on_voice_message()
    async def handle_voice(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return
        if 'handle_voice' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了语音消息。 \n{message}")

    @on_image_message
    async def handle_image(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return
        if 'handle_image' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了图片消息。 \n{message}")

    @on_video_message
    async def handle_video(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return
        if 'handle_video' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了视频消息。 \n{message}")

    @on_file_message
    async def handle_file(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return
        if 'handle_file' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了文件消息。 \n{message}")

    @on_quote_message
    async def handle_quote(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return
        if 'handle_quote' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了引用消息。 \n{message}")

    @on_pat_message
    async def handle_pat(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return
        if 'handle_pat' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了拍一拍消息。 \n{message}")

    @on_emoji_message
    async def handle_emoji(self, bot: WechatAPIClient, message: dict):
        if not self.enable:
            return
        if 'handle_emoji' in self.pushList:
            await self.send_request(message)
        logger.info(f"收到了表情消息。 \n{message}")

    async def send_request(self, message: dict):
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json"
                }
                async with session.post(self.baseUri, headers=headers, json=message, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    logger.info(f"状态码: {response.status}")
                    response_text = await response.text()
                    logger.info(f"响应内容: {response_text}{message}")

                    if response.headers.get('Content-Type') == 'application/json':
                        print("JSON响应:", await response.json())

        except Exception as e:
            logger.warning(f"发送新消息失败 {e}")