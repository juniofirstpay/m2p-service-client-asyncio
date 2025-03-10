import aiohttp
from urllib.parse import urljoin
from typing import List, Dict, Literal, Tuple, Optional, Union
from contextvars import ContextVar
import urllib
from uuid import UUID

# Fix these 2
headers = {}
timeout = 10


base_url_create_account_holder = "account-holder/create"
base_url_get_account_holder = "account-holder/{account_holder_id}"
base_url_get_account_holder_type = "account-holder/vector/{type}/{value}"
base_url_account_holder_otp_action = "account-holder/otp"

base_url_get_accounts = "account/account-holder/{account_holder_id}"
base_url_get_resources = "account-holder/{account_holder_id}/resources"

base_url_create_account = "account/create"
base_url_get_account = "account/{account_id}/details"

base_url_get_account_balance = "account/{account_id}/balance"
base_url_get_funding_account_balance = "account/funding/balance"
base_url_get_account_credit_limit = "account/{account_id}/credit-limit"
base_url_get_account_debit_limit = "account/{account_id}/debit-limit"
base_url_get_account_holder_balance = (
    "account/account-holder/{account_holder_id}/balance"
)
base_url_get_account_holder_token = "account-holder/{account_holder_id}/token"
base_url_get_account_holder_kyc_token = "account-holder/{account_holder_id}/kyc-token"
base_url_account_holder_kyc_upgrade = "/account-holder/{account_holder_id}/kyc/upgrade"
base_url_get_account_holder_kyc_status = "account-holder/{account_holder_id}/kyc-status"

base_url_create_resource = "account/payment-instrument/create"
base_url_get_resource = "account/payment-instrument/{resource_id}"
base_url_resource_id_status = "account/payment-instrument/{resource_id}/status"
base_url_resource_id_delete = "account/payment-instrument/{resource_id}/delete"
base_url_account_transactions = "v2/account/{account_id}/transactions"

base_url_get_resource_via_account_id = "account/{account_id}/payment-instrument"

base_url_form_factor_id = (
    "payment-instrument/{resource_id}/form-factors/{form_factor_id}"
)

base_url_update_account = "account/{account_id}/update"

base_url_account_debit = "transactions/debit"
base_url_account_purchase = "transactions/purchase"
base_url_account_fee = "transactions/fee"
base_url_account_credit = "transactions/credit"
base_url_account_intra_transfer = "transactions/intra-transfer"
base_url_account_inter_transfer = "transactions/inter-transfer"
base_url_account_wallet_transfer = "transactions/wallet-transfer"
base_url_txn_reversal = "transactions/{txn_id}/reversal"
base_url_txn_get = "transactions/{txn_id}/details"

base_url_create_phone_number = (
    "account/{account_id}/payment-instrument/phone-number/create"
)
base_url_delete_phone_number = (
    "account/{account_id}/payment-instrument/phone-number/delete"
)
base_url_create_card = "account/{account_id}/payment-instrument/card/create"
base_url_delete_card = "account/{account_id}/payment-instrument/card/delete"

base_url_get_card = "card/{card_id}/resource"
base_url_get_card_status = "card/{card_id}/status"
base_url_update_card_status = "card/{card_id}/status"
base_url_get_card_view = "card/view"
base_url_get_card_set_pin = "card/set-pin"

base_url_get_txns = "card/resource/{resource_id}/transactions"

base_url_fetch_txn_limit = "accounts/{account_id}/fetch-limit"

base_url_person_account_holder = "person/{person_id}/account-holder"
base_url_person_account_holder_job = "person/{person_id}/account-holder/job"
base_url_person_account = "person/{person_id}/account"
base_url_person_account_details = "person/{person_id}/account/details"
base_url_person_account_job = "person/{person_id}/account/job"
base_url_person_bundle = "person/{person_id}/bundle"
base_url_person_bundle_job = "person/{person_id}/bundle/job"
base_url_person_account_transactions = "person/{person_id}/transactions"
base_url_person_payment_instrument_addon = "person/{person_id}/payment-instrument/add"
base_url_person_payment_instrument_dummy_swap = (
    "person/{person_id}/payment-instrument/dummy-swap"
)
base_url_set_person_account_status = "person/{person_id}/account/status"

base_url_workflow_create_card_dispatch = "workflow/dispatch/card/create"
base_url_workflow_find_card_dispatch = "workflow/dispatch/card/find"
base_url_workflow_get_card_dispatch = "workflow/dispatch/card/{card_dispatch_id}"
base_url_workflow_get_card_dispatch_edit_action = (
    "workflow/dispatch/card/{card_dispatch_id}/edit/action"
)
base_url_workflow_check_zipcode = "workflow/dispatch/zipcode/status"

base_url_create_txn_policy = "policy/{account_holder_id}/{card_id}/create"
base_url_get_txn_policy = "policy/get/{card_id}"
base_url_update_txn_policy = "policy/update/{card_id}"

base_url_card_policy = "card/policy"
base_url_product_inventory = "audit/payment-instrument/inventory"

# def __init__(
#      endpoint: str, client_id: str, client_secret: str, api_key: str, timeout=3
# ):
#     base_url = endpoint
#     client_id = client_id
#     client_secret = client_secret
#     api_key = api_key
#     base_headers = {
#         "ClientId": client_id,
#         "ClientSecret": client_secret,
#         "X-Api-Key": api_key,
#     }

#     timeout = timeout

# def open():
#     request = requests.Session()
#     request.headers.update(base_headers)
#     return

# def close():
#     request.close()
#     request = None
m2p_client_session: ContextVar[aiohttp.ClientSession] = ContextVar(
    "m2p_client_session", default=None
)


async def configure_session(
    base_url: str, dns_cache: bool = True, connection_limit: int = 20
):

    parsed_url = urllib.parse.urlparse(base_url)
    conn = aiohttp.TCPConnector(
        ssl=True if parsed_url.scheme else False,
        use_dns_cache=dns_cache,
        limit=connection_limit,
    )

    session = aiohttp.ClientSession(
        base_url=f"{parsed_url.scheme}://{parsed_url.netloc}", connector=conn
    )

    return session


async def process_response(response: aiohttp.ClientResponse):
    if response.status == 200:
        return (None, await response.json())
    else:
        try:
            response.raise_for_status()
            return (response.status, await response.json())
        except:
            return (response.status, response.text)


async def create_account_holder(*args, **kwargs):
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_create_account_holder, headers=headers, json=kwargs,timeout=timeout
    ) as response:
        return await process_response(response)

    # response = request.post(
    #     url=base_url_create_account_holder,
    #     headers=base_headers,
    #     json=kwargs,
    #     timeout=kwargs.get("timeout",10),
    # )
    # return process_response(response)


async def get_account_holder(type, value, kwargs: dict = {}):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_holder_type.format(type=type, value=value),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_account_holder_via_id(ach_id: str, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_holder.format(account_holder_id=ach_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)
    # response = request.get(
    #     url=urljoin(
    #         base_url,
    #         base_url_get_account_holder.format(account_holder_id=ach_id),
    #     ),
    #     headers=base_headers,
    #     timeout=kwargs.get("timeout",10),
    # )
    # return process_response(response)


async def get_accounts(account_holder_id: str, **kwargs) -> List[Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_holder_type.format(account_holder_id=account_holder_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_account(account_id: str, **kwargs) -> List[Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account.format(account_id=account_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)
    # response = request.get(
    #     url=urljoin(base_url, base_url_get_account.format(account_id=account_id)),
    #     headers=base_headers,
    #     timeout=kwargs.get("timeout",10),
    # )
    # return process_response(response)


# Make the
async def create_account(*args, **kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers",{})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_create_account,
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def get_resources(account_holder_id: str, *args, **kwargs) -> List[Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_resources.format(account_holder_id=account_holder_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_resource_via_account_id(
    account_id: str, *args, **kwargs
) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_resource_via_account_id.format(account_id=account_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_resource(resource_id: str, *args, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_resource.format(resource_id=resource_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)
    # response = request.get(
    #     url=urljoin(
    #         base_url,
    #         base_url_get_resource.format(resource_id=resource_id),
    #     ),
    #     headers=base_headers,
    #     timeout=kwargs.get("timeout",10),
    # )
    # return process_response(response)


async def create_resource(*args, **kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers",{})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_create_resource,
        json=kwargs,
        headers=headers,
        timeout=timeout,
    ) as response:
        return await process_response(response)
    # response = request.post(
    #     url=urljoin(base_url, base_url_create_resource),
    #     headers=base_headers,
    #     json=kwargs,
    #     timeout=kwargs.get("timeout",10),
    # )
    # return process_response(response)


# def get_resource( resource_id: str, *args, **kwargs) -> Dict:
#     response = request.get(
#         url=urljoin(base_url,
#                     base_url_get_resource.format(resource_id=resource_id)),
#         headers=base_headers
#     )
#     if response.status_code == 200:
#         return (None, response.json())
#     else:
#         return (response.status_code, response.json())


async def update_resource_status(resource_id: str, *args, **kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers",{})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_resource_id_status.format(resource_id=resource_id),
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def delete_resource_status(resource_id: str, *args, **kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers",{})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_resource_id_delete.format(resource_id=resource_id),
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def update_form_factor(resource_id: str, form_factor_id: str, **kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers",{})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.put(
        base_url_form_factor_id.format(
            resource_id=resource_id, form_factor_id=form_factor_id
        ),
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def update_account(account_id: str, **kwargs) -> Dict:
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_update_account.format(account_id=account_id),
        headers=kwargs.get("headers", {}),
        json=kwargs,
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def account_debit(**kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_account_debit,
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def account_purchase(**kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_account_purchase,
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def account_fee(**kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_account_fee,
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def account_credit(**kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_account_credit,
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def account_transfer(**kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_account_intra_transfer,
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def account_wallet_transfer(**kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout", 10)
    if kwargs.get("headers"):
        del kwargs["headers"]
    if kwargs.get("timeout"):
        del kwargs["timeout"]
    async with client_session.post(
        base_url_account_wallet_transfer,
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def account_inter_transfer(**kwargs) -> Dict:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_account_inter_transfer,
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def reverse_txn(**kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers", {})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs.get("headers")
    if kwargs.get("timeout"):
        del kwargs.get("timeout")
    async with client_session.post(
        base_url_txn_reversal.format(txn_id=kwargs.get("txn_id")),
        headers=headers,
        json=kwargs,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def get_txn(**kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_txn_get.format(txn_id=kwargs.get("txn_id")),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_balance(account_id: str, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_balance.format(account_id=account_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_funding_account_balance(
    **kwargs,
) -> "Tuple[Optional[int], Dict]":
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_funding_account_balance,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_credit_limit(account_id: str, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_credit_limit.format(account_id=account_id),
        headers={**kwargs.get("headers", {}), "X-API_VERSION": "v1"},
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_debit_limit(**kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_debit_limit.format(account_id=kwargs.get("account_id")),
        headers={**kwargs.get("headers", {}), "X-API-VERSION": "v1"},
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_balance_accounts(**kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_holder_balance.format(
            account_holder_id=kwargs.get("account_holder_id")
        ),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_account_holder_token(**kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_holder_token.format(
            account_holder_id=kwargs.get("account_holder_id")
        ),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_account_holder_kyc_token(
    account_holder_id: str, **kwargs
) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_holder_kyc_token.format(
            account_holder_id=account_holder_id
        ),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def process_account_holder_kyc_upgrade(**kwargs):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_account_holder_kyc_upgrade.format(
            account_holder_id=kwargs.get("account_holder_id")
        ),
        headers=kwargs.get("headers",{}),
        timeout=10,
    ) as response:
        return await process_response(response)


async def get_account_holder_kyc_status(
    account_holder_id: str, **kwargs
) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_account_holder_kyc_status.format(
            account_holder_id=account_holder_id
        ),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def fetch_resource_transactions(**kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_txns.format(resource_id=kwargs.get("resource_id")),
        # headers=kwargs.get("headers",{}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def create_phone_number(
    account_id, phone_number, **kwargs
) -> Tuple[Optional[int], Dict]:
    req_body = {"phone_number": phone_number}
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_create_phone_number.format(account_holder_id=account_id),
        json=req_body,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def delete_phone_number(
    account_id, **kwargs
) -> Tuple[Optional[int], Dict]:
    req_body = {}
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_delete_phone_number.format(account_holder_id=account_id),
        json=req_body,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_account_transactions(
    account_id: str, params: Optional[Dict] = None, **kwargs
) -> Tuple[Optional[int], Union[List, Dict]]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_account_transactions.format(account_id=account_id),
        params=params,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_account_transactions_v2(
    account_id: str, params: Optional[Dict] = None, **kwargs
) -> Tuple[Optional[int], Union[List, Dict]]:
    client_session = m2p_client_session.get()
    url = base_url_account_transactions.format(account_id=account_id)
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    async with client_session.get(
        url,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_person_account_transactions(
    person_id: str, params: Optional[Dict] = None, **kwargs
) -> Tuple[Optional[int], Union[List, Dict]]:
    # url = urljoin(
    #     base_url,
    #     base_url_person_account_transactions.format(person_id=person_id),
    # )
    url = base_url_person_account_transactions.format(person_id=person_id)
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    client_session = m2p_client_session.get()
    async with client_session.get(
        url,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def create_card(account_id, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.post(
        url=base_url_create_card.format(account_id=account_id),
        json={},
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def delete_card(account_id, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    req_body = {}
    async with client_session.get(
        base_url_delete_card.format(account_id=account_id),
        json=req_body,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_card(card_id: str, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_card.format(card_id=card_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_card_view(card_id: str, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_card.format(card_id=card_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_card_view(card_id: str, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_card_view + f"?card_id={card_id}",
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_card_set_pin(card_id: str, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_card_set_pin + f"?card_id={card_id}",
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_card_status(card_id, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_card_status.format(card_id=card_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def update_card_status(
    card_id, status, reason=None, **kwargs
) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    req_body = {
        "card_status": status,
    }
    if reason is not None:
        req_body["reason"] = reason
    async with client_session.get(
        base_url_update_card_status.format(card_id=card_id),
        json=req_body,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def fetch_txn_limit(account_id: str, **kwargs) -> Tuple[Optional[int], Dict]:
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_fetch_txn_limit.format(account_id=account_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_person_account_holder(person_id: "UUID", **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_person_account_holder.format(person_id=person_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_person_account(person_id: "UUID", **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_person_account.format(person_id=person_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_person_account_details(
    person_id: "UUID", account_id: str = None, **kwargs
):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_person_account_details.format(person_id=person_id),
        params={"account_id": account_id},
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_person_bundle(person_id: "UUID", **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_person_bundle.format(person_id=person_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_person_account_holder_job(person_id: "UUID", **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_person_account_holder_job.format(person_id=person_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_person_account_job(person_id: "UUID", **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_person_account_job.format(person_id=person_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_person_bundle_job(person_id: "UUID", **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_person_bundle_job.format(person_id=person_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def create_person_account_holder_job(
    person_id: "UUID" = None, **kwargs
):
    client_session = m2p_client_session.get()
    headers = kwargs.get("headers",{})
    timeout = kwargs.get("timeout",10)
    if kwargs.get("headers"):
        del kwargs["headers"]
    if kwargs.get("timeout"):
        del kwargs["timeout"]
    async with client_session.post(
        base_url_person_account_holder_job.format(person_id=person_id),
        json={
            "attribute": {
                "kyc": {**kwargs, "dob": kwargs.get("dob").strftime("%Y-%m-%d")},
                "proxy": {"account_holder_id": kwargs.get("proxy_ach")},
            }
        },
        headers=headers,
        timeout=timeout,
    ) as response:
        return await process_response(response)


async def create_person_account_job(
    person_id: "UUID" = None, **kwargs
):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_person_account_job.format(person_id=person_id),
        json={
            "attributes": {
                "account_holder_id": kwargs.get("account_holder_id"),
                "account": {
                    "name": kwargs.get("name"),
                },
            }
        },
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def create_person_bundle_job(
    person_id: "UUID" = None, **kwargs
):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_person_bundle_job.format(person_id=person_id),
        json={
            "attributes": {
                "account_holder_id": kwargs.get("account_holder_id"),
                "account": {
                    "name": kwargs.get("name"),
                    "account_id": kwargs.get("account_id"),
                },
                "payment_instrument": {
                    "mobile_number": kwargs.get("mobile_number"),
                },
                "session_id": kwargs.get("session_id"),
                "session_date": kwargs.get("session_date"),
            }
        },
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def create_person_payment_instrument_addon(
    person_id: "UUID" = None,
    payment_instrument_product_code: "str" = None,
    request_ref_id: "str" = None,
    person_type: "str" = None,
    **kwargs
):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_person_payment_instrument_addon.format(person_id=person_id),
        json={
            "payment_instrument_product_code": payment_instrument_product_code,
            "request_ref_id": request_ref_id,
            "person_type": person_type,
        },
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def create_card_dispatch(data: dict, **kwargs: dict):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_workflow_create_card_dispatch,
        json=data,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def find_card_dispatch(params: dict, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_workflow_find_card_dispatch,
        params=params,
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_card_dispatch(card_dispatch_id: str, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_workflow_get_card_dispatch.format(card_dispatch_id=card_dispatch_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def check_zipcode(params, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_workflow_check_zipcode,
        headers={**kwargs.get("headers", {}), "X-Api-Version": "v1"},
        params=params,
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def create_txn_policy(
    account_holder_id, card_id, txn_policy_rules, **kwargs
):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_create_txn_policy.format(
            account_holder_id=account_holder_id, card_id=card_id
        ),
        headers={**kwargs.get("headers", {}), "X-Api-Version": "v1"},
        json=txn_policy_rules,
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_txn_policy(card_id, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_get_txn_policy.format(card_id=card_id),
        headers=kwargs.get("headers", {}),
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def update_txn_policy(card_id, txn_policy_list, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_update_txn_policy.format(card_id=card_id),
        headers=kwargs.get("headers", {}),
        json=txn_policy_list,
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_card_policy(card_id, account_holder_id, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_card_policy,
        headers=kwargs.get("headers", {}),
        params={"card_id": card_id, "account_holder_id": account_holder_id},
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def set_card_policy(card_id, account_holder_id, rules, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_card_policy,
        headers={**kwargs.get("headers", {}), "X-API_VERSION": "v1"},
        json={
            "card_id": card_id,
            "account_holder_id": account_holder_id,
            "data": rules,
        },
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def generate_otp(mobile_number, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_account_holder_otp_action,
        headers={**kwargs.get("headers", {}), "X-API_VERSION": "v1"},
        json={"action": "GENERATE", "request": {"mobile_number": mobile_number}},
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def validate_otp(mobile_number, session_id, user_response, **kwargs):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_account_holder_otp_action,
        headers={**kwargs.get("headers", {}), "X-API_VERSION": "v1"},
        json={
            "action": "VALIDATE",
            "request": {"mobile_number": mobile_number},
            "response": {"user_response": user_response, "session_id": session_id},
        },
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def edit_action_card_dispatch_action(
    card_dispatch_id, action, attributes, **kwargs
):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_workflow_get_card_dispatch_edit_action.format(
            card_dispatch_id=card_dispatch_id
        ),
        headers={**kwargs.get("headers", {}), "X-API_VERSION": "v1"},
        json={"action": action, "attributes": attributes},
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def get_product_inventory(**kwargs):
    client_session = m2p_client_session.get()
    async with client_session.get(
        base_url_product_inventory,
        headers={**kwargs.get("headers", {}), "X-API_VERSION": "v1"},
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def perform_payment_instrument_dummy_swap(
    person_id=None,
    payment_instrument_product_code=None,
    ref_id=None,
    next_ref_id=None,
    person_type=None,
    **kwargs,
):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_person_payment_instrument_dummy_swap.format(person_id=person_id),
        headers={**kwargs.get("headers", {}), "X-API_VERSION": "v1"},
        json={
            "payment_instrument_product_code": payment_instrument_product_code,
            "ref_id": ref_id,
            "next_ref_id": next_ref_id,
            "person_type": person_type,
        },
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)


async def update_person_account_status(
    person_id: str,
    action: Union[Literal["BLOCK"], Literal["UNBLOCK"]],
    reason: str,
    **kwargs,
):
    client_session = m2p_client_session.get()
    async with client_session.post(
        base_url_set_person_account_status.format(person_id=person_id),
        headers={**kwargs.get("headers", {})},
        json={"action": action, "reason": reason},
        timeout=kwargs.get("timeout", 10),
    ) as response:
        return await process_response(response)
