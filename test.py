import sys
sys.path.append('./plugins/')

import plugins
print plugins.get_domain_connection('googlewave.com')
