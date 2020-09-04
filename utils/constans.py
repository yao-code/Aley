# coding: utf-8

# 常量

# 验证码过期时间
IMAGE_CODE_REDIS_EXPIRES = 60 * 1

# 24小时内输入密码错误5次 冻结帐号一天
PASSWORD_ERROR_REDIS_EXPIRES = 60 * 60 *24

# 冻结帐号时间
FREEZE_USER_REDIS_EXPIRES = 60 * 60 * 24
