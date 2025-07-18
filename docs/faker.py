"""
>>> from faker import Faker
>>> fake = Faker()

生成名字
>>> fake.name()
'Kevin Carrillo'
>>> fake.name()
'Annette Thompson'

生成年龄
>>> from datetime import datetime
>>> today = datetime.today()
>>> today
datetime.datetime(2025, 7, 18, 2, 41, 25, 145968)
>>> birth_date = fake.date_of_birth()
>>> birth_date
datetime.date(1979, 8, 8)
>>> age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
>>> age
45
>>>

生成公司名
>>> fake.company()
'Murray PLC'
>>> fake.company()
'Sandoval-Robinson'

书籍名
# 随机生成2到5个词作为标题
num_words = fake.random_int(min=2, max=5)
>>> num_words = fake.random_int(min=2, max=5)
>>> num_words
4
>>> title = ' '.join(fake.words(nb=num_words)).title()
>>> title
'Amount Card During Tend'
>>> fake.words(nb=num_words)
['according', 'the', 'still', 'stuff']
>>>

# pages
>>> pages = fake.random_int(min=120, max=500)
>>> pages
126
>>>

price = fake.pyfloat(
    right_digits=2,  # 确保价格有两位小数
    positive=True,  # 确保价格是正数
    min_value=min_price,  # 设置价格的最小值
    max_value=max_price  # 设置价格的最大值
)
>>> price = fake.pyfloat(right_digits=2, positive=True, min_value=1.0, max_value=2000.0)
>>> price
90.1
>>>

>>> rating = fake.random_int(min=1, max=10)
>>> rating
4
>>>

pubdate = fake.date_of_birth()

>>> dir(fake)
['__annotations__', '__class__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_factories', '_factory_map', '_locales', '_map_provider_method', '_optional_proxy', '_select_factory', '_select_factory_choice', '_select_factory_distribution', '_unique_proxy', '_weights', 'aba', 'add_provider', 'address', 'administrative_unit', 'am_pm', 'android_platform_token', 'ascii_company_email', 'ascii_email', 'ascii_free_email', 'ascii_safe_email', 'bank_country', 'basic_phone_number', 'bban', 'binary', 'boolean', 'bothify', 'bs', 'building_number', 'cache_pattern', 'catch_phrase', 'century', 'chrome', 'city', 'city_prefix', 'city_suffix', 'color', 'color_hsl', 'color_hsv', 'color_name', 'color_rgb', 'color_rgb_float', 'company', 'company_email', 'company_suffix', 'coordinate', 'country', 'country_calling_code', 'country_code', 'credit_card_expire', 'credit_card_full', 'credit_card_number', 'credit_card_provider', 'credit_card_security_code', 'cryptocurrency', 'cryptocurrency_code', 'cryptocurrency_name', 'csv', 'currency', 'currency_code', 'currency_name', 'currency_symbol', 'current_country', 'current_country_code', 'date', 'date_between', 'date_between_dates', 'date_object', 'date_of_birth', 'date_this_century', 'date_this_decade', 'date_this_month', 'date_this_year', 'date_time', 'date_time_ad', 'date_time_between', 'date_time_between_dates', 'date_time_this_century', 'date_time_this_decade', 'date_time_this_month', 'date_time_this_year', 'day_of_month', 'day_of_week', 'del_arguments', 'dga', 'doi', 'domain_name', 'domain_word', 'dsv', 'ean', 'ean13', 'ean8', 'ein', 'email', 'emoji', 'enum', 'factories', 'file_extension', 'file_name', 'file_path', 'firefox', 'first_name', 'first_name_female', 'first_name_male', 'first_name_nonbinary', 'fixed_width', 'format', 'free_email', 'free_email_domain', 'future_date', 'future_datetime', 'generator_attrs', 'get_arguments', 'get_formatter', 'get_providers', 'get_words_list', 'hex_color', 'hexify', 'hostname', 'http_method', 'http_status_code', 'iana_id', 'iban', 'image', 'image_url', 'internet_explorer', 'invalid_ssn', 'ios_platform_token', 'ipv4', 'ipv4_network_class', 'ipv4_private', 'ipv4_public', 'ipv6', 'isbn10', 'isbn13', 'iso8601', 'items', 'itin', 'job', 'job_female', 'job_male', 'json', 'json_bytes', 'language_code', 'language_name', 'last_name', 'last_name_female', 'last_name_male', 'last_name_nonbinary', 'latitude', 'latlng', 'lexify', 'license_plate', 'linux_platform_token', 'linux_processor', 'local_latlng', 'locale', 'locales', 'localized_ean', 'localized_ean13', 'localized_ean8', 'location_on_land', 'longitude', 'mac_address', 'mac_platform_token', 'mac_processor', 'md5', 'military_apo', 'military_dpo', 'military_ship', 'military_state', 'mime_type', 'month', 'month_name', 'msisdn', 'name', 'name_female', 'name_male', 'name_nonbinary', 'nic_handle', 'nic_handles', 'null_boolean', 'numerify', 'opera', 'optional', 'paragraph', 'paragraphs', 'parse', 'passport_dates', 'passport_dob', 'passport_full', 'passport_gender', 'passport_number', 'passport_owner', 'password', 'past_date', 'past_datetime', 'phone_number', 'port_number', 'postalcode', 'postalcode_in_state', 'postalcode_plus4', 'postcode', 'postcode_in_state', 'prefix', 'prefix_female', 'prefix_male', 'prefix_nonbinary', 'pricetag', 'profile', 'provider', 'providers', 'psv', 'pybool', 'pydecimal', 'pydict', 'pyfloat', 'pyint', 'pyiterable', 'pylist', 'pyobject', 'pyset', 'pystr', 'pystr_format', 'pystruct', 'pytimezone', 'pytuple', 'random', 'random_choices', 'random_digit', 'random_digit_above_two', 'random_digit_not_null', 'random_digit_not_null_or_empty', 'random_digit_or_empty', 'random_element', 'random_elements', 'random_int', 'random_letter', 'random_letters', 'random_lowercase_letter', 'random_number', 'random_sample', 'random_uppercase_letter', 'randomize_nb_elements', 'rgb_color', 'rgb_css_color', 'ripe_id', 'safari', 'safe_color_name', 'safe_domain_name', 'safe_email', 'safe_hex_color', 'sbn9', 'secondary_address', 'seed', 'seed_instance', 'seed_locale', 'sentence', 'sentences', 'set_arguments', 'set_formatter', 'sha1', 'sha256', 'simple_profile', 'slug', 'ssn', 'state', 'state_abbr', 'street_address', 'street_name', 'street_suffix', 'suffix', 'suffix_female', 'suffix_male', 'suffix_nonbinary', 'swift', 'swift11', 'swift8', 'tar', 'text', 'texts', 'time', 'time_delta', 'time_object', 'time_series', 'timezone', 'tld', 'tsv', 'unique', 'unix_device', 'unix_partition', 'unix_time', 'upc_a', 'upc_e', 'uri', 'uri_extension', 'uri_page', 'uri_path', 'url', 'user_agent', 'user_name', 'uuid4', 'vin', 'weights', 'windows_platform_token', 'word', 'words', 'xml', 'year', 'zip', 'zipcode', 'zipcode_in_state', 'zipcode_plus4']
>>>
>>>

"""