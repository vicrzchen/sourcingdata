SERVER_ADDRESS = 'localhost'
SERVER_PORT = '3306'
DB_USER = 'root'
DB_PASSWORD = '!234Qwer'
DB_NAME = 'sourcingdata'
CHARSET = 'utf8'
REQUIREMENT_TO_BE_READ_TABLE_NAME = 'requirement_to_read'

# URL message
START_URL_REQUIREMENT_TO_BE_READ = 'http://www.gdgpo.gov.cn/organization/querySellerOrgList.html'
START_URL_SOURCING_ANNOUNCEMENT_TO_BE_READ = 'http://www.gdgpo.gov.cn/queryMoreInfoList/channelCode/0005.html'
START_URL_CONTRACT_INFO_TO_BE_READ = 'http://www.gdgpo.gov.cn/queryContractList.html'

# Next page string
NEXT_PAGE_OF_REQUIREMENT_TO_BE_READ = '//a[@class="aborder2"]/span[contains(.,"下一页")]'
NEXT_PAGE_OF_SOURCING_ANNOUNCEMENT_TO_BE_READ = '//a[@class="aborder2"]/span[contains(.,"下一页")]'
NEXT_PAGE_OF_CONTRACT_INFO_TO_BE_READ = '//a[@class="aborder2"]/span[contains(.,"下一页")]'

# Next page time interval
TIME_INTERVAL_MIN_SECOND_SOURCING_ANNOUNCEMENT_TO_BE_READ = 0
TIME_INTERVAL_MAX_SECOND_SOURCING_ANNOUNCEMENT_TO_BE_READ = 0

USE_PROXY = False
