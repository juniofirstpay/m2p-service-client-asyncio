import uuid
from datetime import datetime
from typing import Dict, List, Literal, Tuple, Optional, Union
from uuid import UUID
from .schema import (
    CreateAccountSchema,
    CreateAccountHolderSchema,
    CreateResourceSchema,
    DeleteResourceStatusSchema,
    PersonAccountHolderSchema,
    PersonAccountSchema,
    PersonBundleSchema,
    PersonDummySwapPaymentInstrumentSchema,
    UpdateFormFactorStatusSchema,
    UpdateResourceStatusSchema,
    AccountCreditSchema,
    AccountDebitSchema,
    AccountTransferSchema,
    AccountWalletTransferSchema,
)
import m2p_micro_client.service as m2p_service


async def create_account_holder(
    first_name: str,
    middle_name: str,
    last_name: str,
    date_of_birth: str,
    gender: str,
    kyc_type: str,
    kyc_value: str,
    phone_number: str,
    person_id: uuid = None,
) -> Dict:
    data = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "dob": date_of_birth,
        "gender": gender,
        "kyc_type": kyc_type,
        "kyc_value": kyc_value,
        "phone_number": phone_number,
        "person_id": person_id,
    }
    valid_data = CreateAccountHolderSchema().load(data)
    if valid_data.get("person_id"):
        valid_data["person_id"] = str(valid_data.get("person_id"))
    dob = valid_data.pop("dob")
    phone_number = "+91" + valid_data.pop("phone_number")
    response = await m2p_service.create_account_holder(
        **valid_data, phone_number=phone_number, dob=dob.isoformat()
    )
    return response


async def get_account_holder(type: str, value: str):
    response = await m2p_service.get_account_holder(type, value)
    return response


async def get_account_holder_via_id(ach_id: str):
    response = await m2p_service.get_account_holder_via_id(ach_id)
    return response


async def get_accounts(account_holder_id: str) -> List[Dict]:
    response = await m2p_service.get_accounts(account_holder_id)
    return response


async def get_account(account_id: str) -> List[Dict]:
    response = await m2p_service.get_account(account_id)
    return response


async def update_account(account_id: str, status: str) -> List[Dict]:
    response = await m2p_service.update_account(account_id, status=status)
    return response


# Make the
async def create_account(
    account_holder_id: str, account_name: str, person_id: uuid = None
) -> Dict:
    data = {
        "account_holder_id": account_holder_id,
        "accounts": [account_name],
        "person_id": person_id,
    }
    valid_data = CreateAccountSchema().load(data)
    if valid_data.get("person_id"):
        valid_data["person_id"] = str(valid_data.get("person_id"))
    (error, response) = await m2p_service.create_account(**valid_data)
    if error:
        return error, response
    return (None, response[0])


async def get_resources(account_holder_id: str) -> List[Dict]:
    response = await m2p_service.get_resources(account_holder_id)
    return response


async def get_resource(resource_id: str) -> Tuple[Optional[int], Dict]:
    response = await m2p_service.get_resource(resource_id)
    return response


async def get_resource_via_account_id(account_id: str) -> Tuple[Optional[int], Dict]:
    response = await m2p_service.get_resource_via_account_id(account_id)
    return response


async def create_resource(account_id: str, mobile_number: str, person_id=None) -> Dict:

    data = {
        "account_id": account_id,
        "phone_number": mobile_number,
        "person_id": person_id,
    }
    valid_data = CreateResourceSchema().load(data)
    if valid_data.get("person_id"):
        valid_data["person_id"] = str(valid_data.get("person_id"))
    response = await m2p_service.create_resource(**valid_data)
    return response


async def get_resource(resource_id: str) -> Dict:
    response = await m2p_service.get_resource(resource_id)
    return response


async def update_resource_status(
    resource_id: str, status: str, description: str
) -> Dict:
    data = {"status": status, "description": description}
    valid_data = UpdateResourceStatusSchema().load(data)
    response = await m2p_service.update_resource_status(resource_id, **valid_data)
    return response


async def delete_resource(resource_id: str, description: str) -> Dict:
    data = {"status": "DELETED"}
    valid_data = DeleteResourceStatusSchema().load(data)
    response = await m2p_service.delete_resource_status(resource_id, **valid_data)
    return response


async def update_form_factor(
    resource_id: str, form_factor_id: str, status: str, description: str
) -> Dict:
    data = {"status": status, "description": description}
    valid_data = UpdateFormFactorStatusSchema().load(data)
    response = await m2p_service.update_form_factor(
        resource_id, form_factor_id, **valid_data
    )
    return response


async def debit_account(
    txn_id: str, account_id: str, amount: int, remarks: str, attributes: dict
):

    data = {
        "debit_account_id": account_id,
        "amount": amount,
        "remarks": remarks,
        "attributes": attributes,
        "txn_id": txn_id,
    }
    valid_data = AccountDebitSchema().load(data)
    response = await m2p_service.account_debit(**valid_data)
    return response


async def purchase_on_account(
    txn_id: str, account_id: str, amount: int, remarks: str, attributes: dict
):

    data = {
        "debit_account_id": account_id,
        "amount": amount,
        "remarks": remarks,
        "attributes": attributes,
        "txn_id": txn_id,
    }
    valid_data = AccountDebitSchema().load(data)
    response = await m2p_service.account_purchase(**valid_data)
    return response


async def fee_on_account(
    txn_id: str, account_id: str, amount: int, remarks: str, attributes: dict
):

    data = {
        "debit_account_id": account_id,
        "amount": amount,
        "remarks": remarks,
        "attributes": attributes,
        "txn_id": txn_id,
    }
    valid_data = AccountDebitSchema().load(data)
    response = await m2p_service.account_fee(**valid_data)
    return response


async def credit_account(
    txn_id: str,
    account_id: str,
    amount: int,
    remarks: str,
    attributes: dict,
):

    data = {
        "credit_account_id": account_id,
        "amount": amount,
        "remarks": remarks,
        "attributes": attributes,
        "txn_id": txn_id,
    }
    valid_data = AccountCreditSchema().load(data)
    response = await m2p_service.account_credit(**valid_data)
    return response


async def account_transfer(
    txn_id: str,
    debit_account_id: str,
    credit_account_id: str,
    amount: int,
    remarks: str,
    attributes: dict,
):

    data = {
        "debit_account_id": debit_account_id,
        "credit_account_id": credit_account_id,
        "amount": amount,
        "remarks": remarks,
        "attributes": attributes,
        "txn_id": txn_id,
    }
    valid_data = AccountTransferSchema().load(data)
    response = await m2p_service.account_transfer(**valid_data)
    return response


async def account_inter_transfer(
    txn_id: str,
    debit_account_id: str,
    credit_account_id: str,
    amount: int,
    remarks: str,
    attributes: dict,
):

    data = {
        "debit_account_id": debit_account_id,
        "credit_account_id": credit_account_id,
        "amount": amount,
        "remarks": remarks,
        "attributes": attributes,
        "txn_id": txn_id,
    }
    valid_data = AccountTransferSchema().load(data)
    response = await m2p_service.account_inter_transfer(**valid_data)
    return response


async def account_wallet_transfer(
    txn_id: str,
    account_id: str,
    amount: int,
    remarks: str,
    attributes: dict,
):

    data = {
        "account_id": account_id,
        "amount": amount,
        "remarks": remarks,
        "attributes": attributes,
        "txn_id": txn_id,
    }
    valid_data = AccountWalletTransferSchema().load(data)
    response = await m2p_service.account_wallet_transfer(**valid_data)
    return response


async def get_txn(txn_id: str):
    response = await m2p_service.get_txn(txn_id=txn_id)
    return response


async def reverse_txn(txn_id: str, remarks=None):
    response = await m2p_service.reverse_txn(txn_id=txn_id, remarks=remarks)
    return response


async def get_balance(account_id: str):
    response = await m2p_service.get_balance(account_id=account_id)
    return response


async def get_funding_account_balance():
    return await m2p_service.get_funding_account_balance()


async def get_credit_limit(account_id: str):
    response = await m2p_service.get_credit_limit(
        account_id=account_id, timeout=(3.05, 3.05)
    )
    return response


async def get_debit_limit(account_id: str):
    response = await m2p_service.get_debit_limit(account_id=account_id)
    return response


async def get_balance_accounts(account_holder_id: str):
    response = await m2p_service.get_balance_accounts(
        account_holder_id=account_holder_id
    )
    return response


async def get_account_holder_token(account_holder_id: str):
    response = await m2p_service.get_account_holder_token(
        account_holder_id=account_holder_id
    )
    return response


async def get_account_holder_kyc_token(account_holder_id: str):
    response = await m2p_service.get_account_holder_kyc_token(
        account_holder_id=account_holder_id
    )
    return response


async def process_account_holder_kyc_upgrade(account_holder_id: str):
    response = await m2p_service.process_account_holder_kyc_upgrade(
        account_holder_id=account_holder_id
    )
    return response


async def get_account_holder_kyc_status(account_holder_id: str):
    response = await m2p_service.get_account_holder_kyc_status(
        account_holder_id=account_holder_id
    )
    return response


async def get_resource_txns(resource_id: str):
    response = await m2p_service.fetch_resource_transactions(resource_id=resource_id)
    return response


async def create_phone_number(account_id: str, phone_number: str):
    response = await m2p_service.create_phone_number(
        account_id=account_id, phone_number=phone_number
    )
    return response


async def delete_phone_number(account_id: str):
    response = await m2p_service.delete_phone_number(account_id=account_id)
    return response


async def get_account_transactions(account_id: str, params: Optional[Dict] = None):
    response = await m2p_service.get_account_transactions(
        account_id=account_id, params=params
    )
    return response


async def get_account_transactions_v2(account_id: str, params: Optional[Dict] = None):
    response = await m2p_service.get_account_transactions_v2(
        account_id=account_id, params=params
    )
    return response


async def get_person_account_transaction(person_id: str, params: Optional[Dict] = None):
    return await m2p_service.get_person_account_transactions(
        person_id=person_id, params=params
    )


async def create_card(account_id: str):
    response = await m2p_service.create_card(account_id=account_id)
    return response


async def delete_card(account_id: str):
    response = await m2p_service.delete_card(account_id=account_id)
    return response


async def get_card(card_id: str):
    return await m2p_service.get_card(card_id=card_id)


async def get_card_view(card_id: str):
    return await m2p_service.get_card_view(card_id=card_id)


async def get_card_set_pin(card_id: str):
    return await m2p_service.get_card_set_pin(card_id=card_id)


async def get_card_status(card_id):
    response = await m2p_service.get_card_status(card_id=card_id)
    return response


async def update_card_status(card_id, status, reason=None):
    response = await m2p_service.update_card_status(
        card_id=card_id, status=status, reason=reason
    )
    return response


async def fetch_txn_limit(account_id: str):
    response = await m2p_service.fetch_txn_limit(account_id=account_id)
    return response


async def create_card_dispatch(
    person_id: "uuid.UUID",
    order_id: str,
    dispatcher: str,
    card_form_factor_id: str,
    customer: dict,
    receiver: dict,
    delivery_address: dict,
    card_attributes: dict,
    dispatch_status: str = None,
):
    from .schema import CreateCardDispatchSchema

    data = {
        "person_id": person_id,
        "order_id": order_id,
        "dispatcher": dispatcher,
        "card_form_factor_id": card_form_factor_id,
        "customer": customer,
        "receiver": receiver,
        "delivery_address": delivery_address,
        "card_attributes": card_attributes,
        "dispatch_status": dispatch_status,
    }

    if dispatch_status:
        data["dispatch_status"] = dispatch_status

    valid_data = CreateCardDispatchSchema().load(data)

    valid_data["person_id"] = str(person_id)
    valid_data["customer"]["person_id"] = str(valid_data["customer"]["person_id"])
    valid_data["receiver"]["person_id"] = str(valid_data["receiver"]["person_id"])

    return await m2p_service.create_card_dispatch(**valid_data)


async def find_card_dispatch(
    person_id: str,
    card_form_factor_id: str,
    secondary_person_id: str = None,
    realtime=False,
):
    return await m2p_service.find_card_dispatch(
        person_id=person_id,
        card_form_factor_id=card_form_factor_id,
        secondary_person_id=secondary_person_id,
        realtime=realtime,
    )


async def get_card_dispatch(card_dispatch_id: str):
    return await m2p_service.get_card_dispatch(card_dispatch_id)


async def edit_card_dispatch_action(
    card_dispatch_id: str, action: str, attributes: dict
):
    return await m2p_service.edit_action_card_dispatch_action(
        card_dispatch_id, action, attributes
    )


async def check_zipcode(zipcode: str):
    return await m2p_service.check_zipcode(params={"zipcode": zipcode})


# async def reissue_card_form_factor(
#
#     child_account_id: str,
#     parent_account_id: str,
#     child_phone_number: str,
#     resource_id: str
# ):
#     # Fetch old account
#     error, old_account = get_account(child_account_id)
#     print("error, old_account", error, old_account)
#     if error:
#         return error, "Child account not found."

#     # Fetch old balance
#     error, old_balance = get_balance(old_account["zeta_ref_id"])
#     print("error, old_balance", error, old_balance)
#     if error:
#         return error, "Balance fetch error."

#     # Get resource
#     error, old_resource = get_resource(resource_id)
#     print("error, old_resource", error, old_resource)
#     if error:
#         return error, "Old resource not found."

#     if old_resource["account_id"] != child_account_id:
#         return 400, "Resource mismatch error."

#     # Delete old card
#     # error, old_card = delete_card(child_account_id)
#     # print("error, old_card", error, old_card)
#     # if error:
#     #     return error, "Old card deletion error."

#     # Delete old number
#     # error, old_phone_number = delete_phone_number(child_account_id)
#     # print("error, old_phone_number", error, old_phone_number)
#     # if error:
#     #     return error, "Old phone number deletion error."

#     # Create new account
#     error, new_account = create_account(
#         old_account["owner_ach_id"],
#         f'{old_account["name"]}_1'
#     )


async def get_person_account_holder(person_id: "UUID"):
    return await m2p_service.get_person_account_holder(person_id)


async def get_person_account(person_id: "UUID"):
    return await m2p_service.get_person_account(person_id)


async def get_person_account_details(person_id: "UUID", account_id: str = None):
    return await m2p_service.get_person_account_details(
        person_id, account_id=account_id
    )


async def get_person_bundle(person_id: "UUID"):
    return await m2p_service.get_person_bundle(person_id)


async def get_person_account_holder_job(person_id: "UUID"):
    return await m2p_service.get_person_account_holder_job(person_id)


async def get_person_account_job(person_id: "UUID"):
    return await m2p_service.get_person_account_job(person_id)


async def get_person_bundle_job(person_id: "UUID"):
    return await m2p_service.get_person_bundle_job(person_id)


async def create_person_account_holder_job(
    person_id: "UUID",
    first_name: str,
    middle_name: str,
    last_name: str,
    dob: str,
    gender: str,
    mobile_number: str,
    auth_type: str = None,
    auth_data: str = None,
    session_id: "Optional[str]" = None,
    session_date: "Optional[datetime]" = None,
    proxy_ach: str = None,
):

    valid_data = PersonAccountHolderSchema().load(
        {
            "person_id": person_id,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "dob": dob,
            "gender": gender,
            "mobile_number": mobile_number,
            "auth_type": auth_type,
            "auth_data": auth_data,
            "proxy_ach": proxy_ach,
            "session_id": session_id,
            "session_date": session_date,
        }
    )

    return await m2p_service.create_person_account_holder_job(**valid_data)


async def create_person_account_job(
    person_id: "UUID", account_holder_id: str, account_name: str
):
    valid_data = PersonAccountSchema().load(
        {
            "person_id": person_id,
            "account_holder_id": account_holder_id,
            "name": account_name,
        }
    )
    return await m2p_service.create_person_account_job(**valid_data)


async def create_person_bundle_job(
    person_id: "UUID",
    account_holder_id: str,
    account_name: str,
    mobile_number: str,
    account_id: Optional[str] = None,
    session_id: "Optional[str]" = None,
    session_date: "Optional[datetime]" = None,
):
    valid_data = PersonBundleSchema().load(
        {
            "person_id": person_id,
            "account_holder_id": account_holder_id,
            "name": account_name,
            "mobile_number": mobile_number,
            "account_id": account_id,
            "session_id": session_id,
            "session_date": session_date,
        }
    )
    return await m2p_service.create_person_bundle_job(**valid_data)


async def create_person_payment_instrument_addon(
    person_id: "uuid.UUID",
    payment_instrument_product_code: "str",
    request_ref_id,
    person_type: "str",
):
    return await m2p_service.create_person_payment_instrument_addon(
        person_id, payment_instrument_product_code, request_ref_id, person_type
    )


async def create_txn_policy(
    account_holder_id: uuid, card_id: uuid, txn_policy_rules: list
):
    return await m2p_service.create_txn_policy(
        account_holder_id, card_id, txn_policy_rules
    )


async def get_txn_policy(card_id: uuid):
    return await m2p_service.get_txn_policy(card_id)


async def update_txn_policy(card_id: uuid, txn_policy_list: list):
    return await m2p_service.update_txn_policy(card_id, txn_policy_list)


async def get_card_policy(card_id: str, account_holder_id: str):
    return await m2p_service.get_card_policy(card_id, account_holder_id)


async def set_card_policy(card_id: str, account_holder_id: str, rules):
    return await m2p_service.set_card_policy(card_id, account_holder_id, rules)


async def generate_otp(mobile_number: str):
    return await m2p_service.generate_otp(mobile_number)


async def validate_otp(mobile_number: str, session_id: str, otp: str):
    return await m2p_service.validate_otp(mobile_number, session_id, otp)


async def get_product_inventory():
    return await m2p_service.get_product_inventory()


async def perform_person_payment_instrument_dummy_swap(
    person_id: "uuid.UUID",
    payment_instrument_product_code: "str",
    ref_id: "str",
    next_ref_id: "str",
    person_type: "str",
):
    valid_data = PersonDummySwapPaymentInstrumentSchema().load(
        {
            "person_id": person_id,
            "payment_instrument_product_code": payment_instrument_product_code,
            "ref_id": ref_id,
            "next_ref_id": next_ref_id,
            "person_type": person_type,
        }
    )
    return await m2p_service.perform_payment_instrument_dummy_swap(**valid_data)


async def update_person_account_status(
    person_id: str,
    action: Union[Literal["BLOCK"], Literal["UNBLOCK"]],
    reason: str,
):
    return await m2p_service.update_person_account_status(person_id, action, reason)
