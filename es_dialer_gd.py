import requests

import common
import payload
from config import Config


def build_headers(
        cdc_domain=None, cdc_school_id=None, cdc_area=None,
        user_agent=None, algo_id=None, client_id=None,
        cdc_checksum=None):
    headers = {}

    if cdc_domain is not None:
        headers['CDC-Domain'] = cdc_domain
    if cdc_school_id is not None:
        headers['CDC-SchoolId'] = cdc_school_id
    if cdc_area is not None:
        headers['CDC-Area'] = cdc_area
    if user_agent is not None:
        headers['User-Agent'] = user_agent
    if client_id is not None:
        headers['Client-ID'] = client_id
    if algo_id is not None:
        headers['Algo-ID'] = algo_id
    if cdc_checksum is not None:
        headers['CDC-Checksum'] = cdc_checksum

    return headers


class EsDialerGD:
    def __init__(self):
        self._info = Config.load_data('info.json', {})
        self._config = Config.load_data('config.json', None)
        if self._config is None:
            raise Exception('Can not load config.')
        else:
            print(self._config)

    def init(self):
        config = self._config
        info = self._info

        headers = build_headers(user_agent=config.get('user_agent'))
        try:
            resp = requests.get('http://baidu.com', headers=headers, timeout=3)
            resp_str = resp.content.decode('gbk', errors='ignore')

            index_url = resp.url
            if 'index.cgi' in index_url:
                info['index_url'] = index_url
            elif info.get('index_url') is not None:
                resp = requests.get(info['index_url'], headers=headers)
                resp_str = resp.content.decode('gbk', errors='ignore')

            ticket_url = common.get_tag_content(resp_str, 'ticket-url')
            auth_url = common.get_tag_content(resp_str, 'auth-url')

            result = ticket_url != '' and auth_url != ''
            if result:
                info['ticket_url'] = ticket_url
                info['auth_url'] = auth_url

                ipv4_addr = common.str_extract(resp_str, 'wlanuserip=', '&')
                if ipv4_addr == '':
                    ipv4_addr = common.str_extract(resp_str, 'wlanuserip=', '"')

                info['ipv4_addr'] = ipv4_addr
                Config.dump_data('info.json', self._info)
        except Exception as e:
            print('[init] %s' % e)
            result = False

        return result

    def _update_time(self):
        info = self._info
        info['local_time'] = common.now_str()

    def _build_headers(self, cdc_checksum=None):
        config = self._config
        headers = build_headers(
            cdc_domain=config.get('cdc_domain', "szpt"),
            cdc_school_id=config.get('cdc_school_id', "113"),
            cdc_area=config.get('cdc_area', "0755"),
            user_agent=config.get('user_agent', "CCTP/mac1/5007"),
            algo_id=config.get('algo_id', "54EB0E0D-58FE-46E2-8629-0A517E2785F4"),
            client_id=config.get('client_id', "2CDEABEA-BA33-5C55-9DCA-C8F0337897EA"),
            cdc_checksum=cdc_checksum
        )

        return headers

    def _get_ticket(self):
        config = self._config
        info = self._info

        data = payload.build_ticket_payload(
            config.get('host_name'),
            config.get('user_agent'),
            config.get('client_id'),
            info['ipv4_addr'],
            '',
            config.get('mac_addr'),
            config.get('ostag'),
            info['local_time']
        )
        cdc_checksum = common.md5_str(data)
        headers = self._build_headers(cdc_checksum)

        resp = requests.post(info['ticket_url'], data.encode('utf8'), headers=headers)
        resp_str = resp.content.decode('utf8')
        resp_str_raw = payload.payload_decode(resp_str)

        info['ticket'] = common.get_tag_content(resp_str_raw, 'ticket')

        result = info['ticket'] != ''
        if result:
            print('[ticket] %s' % info['ticket'])

        return result

    def auth(self):
        config = self._config
        info = self._info

        self._update_time()
        result = self._get_ticket()
        if result:
            self._update_time()

            data = payload.build_auth_payload(
                config.get('user_id'),
                config.get('passwd'),
                info['ticket'],
                config.get('client_id'),
                config.get('host_name'),
                config.get('user_agent'),
                info['local_time']
            )
            cdc_checksum = common.md5_str(data)

            headers = self._build_headers(cdc_checksum)

            resp = requests.post(info['auth_url'], data.encode('utf8'), headers=headers)
            resp_str = resp.content.decode('utf8', errors='ignore')
            resp_str_raw = payload.payload_decode(resp_str)

            keep_url = common.get_tag_content(resp_str_raw, 'keep-url')
            term_url = common.get_tag_content(resp_str_raw, 'term-url')

            info['keep_url'] = keep_url
            info['term_url'] = term_url

            result = keep_url != '' and term_url != ''
            print(self._info)
            if result:
                Config.dump_data('info.json', self._info)
            else:
                print('[auth] %s' % resp_str_raw)

        return result

    def keep(self):
        config = self._config
        info = self._info

        self._update_time()
        data = payload.build_keep_payload(
            config.get('user_agent'),
            info['local_time'],
            info['ticket'],
            config.get('host_name'),
            config.get('client_id')
        )
        cdc_checksum = common.md5_str(data)
        headers = self._build_headers(cdc_checksum)

        resp = requests.post(info['keep_url'], data.encode('utf8'), headers=headers)
        resp_str = resp.content.decode('utf8')
        resp_str_raw = payload.payload_decode(resp_str)

        result = -1
        interval = common.get_tag_content(resp_str_raw, 'interval')
        if interval != '':
            result = int(interval)
        else:
            print('[keep] %s' % resp_str_raw)

        return result

    def term(self):
        config = self._config
        info = self._info

        self._update_time()
        data = payload.build_term_payload(
            config.get('user_agent'),
            info['ticket'],
            info['local_time'],
            config.get('host_name'),
            config.get('client_id')
        )
        cdc_checksum = common.md5_str(data)
        headers = self._build_headers(cdc_checksum)

        try:
            requests.post(info['term_url'], data.encode('utf8'), headers=headers, timeout=3)
        except Exception as e:
            print('[term] %s' % e)
