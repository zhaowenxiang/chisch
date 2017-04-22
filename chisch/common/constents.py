# coding: utf-8

USER_STATUS_INACTIVE = 0                        # 用户异常状态
USER_STATUS_ACTIVE = 1                          # 用户正常状态

VERIFY_CODE_LENGTH = 6                          # 验证码长度

VERIFY_TYPE_LOGIN = 1                           # 验证类型：登陆
VERIFY_TYPE_REGISTER = 2                        # 验证类型：注册
VERIFY_TYPE_CHANGE_PASSWORD = 3                 # 验证类型：修改密码

VERIFY_TYPE_OPERATE_MAP = {
    VERIFY_TYPE_LOGIN: '登陆',
    VERIFY_TYPE_REGISTER: '注册',
    VERIFY_TYPE_CHANGE_PASSWORD: '修改密码'
}

VERIFY_CODE_EFFECTIVE_TIME = 600                 # 验证码有效期10分钟
VERIFY_CODE_GET_INTERVAL = 60                   # 获取验证码时间间隔
VERIFY_UPPER_LIMIT_BY_IP = 10                   # 每个IP每天获取验证码的上限次数
VERIFY_UPPER_LIMIT_BY_USER_NAME = 10            # 每个IP每天获取验证码的上限次数
VERIFY_STATISTIC_WAY_USER_NAME = 1              # user_name验证统计
VERIFY_STATISTIC_WAY_IP = 2                     # IP验证统计

TOKEN_EFFECTIVE_TIME = 15                       # token有效期为15天
TOKEN_INVALID_REASON_UNRECOGNIZED = 0           # 无法识别token
TOKEN_INVALID_REASON_EXPIRE = 1                 # token有效期已满
TOKEN_INVALID_REASON_LOGIN_OTHER_PLACE = 2      # 同种设备异地登陆，导致该token失效