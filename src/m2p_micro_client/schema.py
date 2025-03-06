from marshmallow import Schema, fields, validate


class CreateAccountHolderSchema(Schema):
    first_name = fields.Str(
        required=True, allow_none=False, validate=validate.Length(min=1)
    )
    middle_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    gender = fields.Str(required=True, validate=validate.OneOf(["Male", "Female"]))
    kyc_type = fields.Str(
        required=True,
        validate=validate.OneOf(["VOTER_ID", "PAN", "PASSPORT", "DRIVING_LICENSE"]),
    )
    kyc_value = fields.Str(required=True, validate=validate.Length(min=5))
    phone_number = fields.Str(required=True, validate=validate.Length(equal=10))
    dob = fields.Date(required=True)
    person_id = fields.UUID(required=False, allow_none=True)
    session_id = fields.String(required=False, allow_none=True)


class CreateAccountSchema(Schema):
    account_holder_id = fields.Str(required=True)
    accounts = fields.List(fields.Str(required=True, validate=validate.Length(min=5)))
    person_id = fields.UUID(required=False, allow_none=True)


class CreateResourceSchema(Schema):
    account_id = fields.Str(required=True, validate=validate.Length(equal=36))
    phone_number = fields.Str(required=True, validate=validate.Length(equal=13))
    person_id = fields.UUID(required=False, allow_none=True)


class UpdateResourceStatusSchema(Schema):
    status = fields.Str(
        required=True, validate=validate.OneOf(["ACTIVE", "INACTIVE", "DELETED"])
    )
    description = fields.Str()


class DeleteResourceStatusSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(["DELETED"]))


class UpdateFormFactorStatusSchema(Schema):
    status = fields.Str(
        required=True, validate=validate.OneOf(["ACTIVE", "INACTIVE", "DELETED"])
    )
    description = fields.Str()


class SuspendAccountSchema(Schema):
    status = fields.Str(required=True)


class AccountDebitSchema(Schema):
    debit_account_id = fields.Str(required=True)
    amount = fields.Integer(required=True)
    remarks = fields.Str(required=True)
    attributes = fields.Dict(keys=fields.String(), values=fields.String())
    txn_id = fields.Str(required=True)


class AccountCreditSchema(Schema):
    credit_account_id = fields.Str(required=True)
    amount = fields.Integer(required=True)
    remarks = fields.Str(required=True)
    attributes = fields.Dict(keys=fields.String(), values=fields.String())
    txn_id = fields.Str(required=True)


class AccountTransferSchema(Schema):
    debit_account_id = fields.Str(required=True)
    credit_account_id = fields.Str(required=True)
    amount = fields.Integer(required=True)
    remarks = fields.Str(required=True)
    attributes = fields.Dict(keys=fields.String(), values=fields.String())
    txn_id = fields.Str(required=True)


class AccountWalletTransferSchema(Schema):
    account_id = fields.Str(required=True)
    amount = fields.Integer(required=True)
    remarks = fields.Str(required=True)
    attributes = fields.Dict(keys=fields.String(), values=fields.String())
    txn_id = fields.Str(required=True)


class PersonAccountHolderSchema(Schema):

    person_id = fields.UUID(required=True)
    first_name = fields.String(required=True)
    middle_name = fields.String(required=True)
    last_name = fields.String(required=True)
    dob = fields.Date(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(["Male", "Female"]))
    mobile_number = fields.String(required=True, validate=validate.Length(10))
    auth_type = fields.String(
        required=True,
        validate=validate.OneOf(["PAN", "DRIVING_LICENSE", "VOTER_ID", "PASSPORT"]),
    )
    auth_data = fields.String(required=True, min=5)
    proxy_ach = fields.String(required=False, allow_none=True)
    session_id = fields.String(required=False, allow_none=True)
    session_date = fields.String(required=False, allow_none=True)


class PersonAccountSchema(Schema):

    person_id = fields.UUID(required=True)
    account_holder_id = fields.String(required=True)
    name = fields.String(required=True)


class PersonBundleSchema(Schema):

    person_id = fields.UUID(required=True)
    account_holder_id = fields.String(required=True)
    name = fields.String(required=True)
    mobile_number = fields.String(required=True)
    account_id = fields.String(allow_none=True)
    session_id = fields.String(required=False, allow_none=True)
    session_date = fields.String(required=False, allow_none=True)


class PersonDummySwapPaymentInstrumentSchema(Schema):

    person_id = fields.String(required=True)
    payment_instrument_product_code = fields.String(required=True)
    ref_id = fields.String(required=True)
    next_ref_id = fields.String(required=True)
    person_type = fields.String(required=False)


class CreateCardDispatchSchema(Schema):
    class CardDispatchPersonSchema(Schema):
        person_id = fields.UUID(required=True, allow_none=False)
        name = fields.String(required=True, allow_none=False)
        mobile_number = fields.String(required=True, validate=validate.Length(equal=10))

    class CardDispatchAddressSchema(Schema):
        address_line_1 = fields.String(required=True, allow_none=False)
        address_line_2 = fields.String(required=True, allow_none=False)
        address_line_3 = fields.String(required=True, allow_none=False)
        address_line_4 = fields.String(required=True, allow_none=False)
        city = fields.String(required=True, allow_none=False)
        state = fields.String(required=True, allow_none=False)
        zipcode = fields.String(required=True, allow_none=False)

    class CardDispatchAttributesSchema(Schema):

        card_name_1 = fields.String(required=True, allow_none=False)
        card_name_2 = fields.String(required=True, allow_none=True)

    person_id = fields.UUID(required=True, allow_none=False)
    order_id = fields.String(required=True, allow_none=True)
    dispatcher = fields.String(
        required=True, validate=validate.OneOf(["DJANGO", "DOTNET"])
    )
    card_form_factor_id = fields.Str(required=True, allow_none=True)
    customer = fields.Nested(CardDispatchPersonSchema)
    receiver = fields.Nested(CardDispatchPersonSchema)
    delivery_address = fields.Nested(CardDispatchAddressSchema)
    card_attributes = fields.Nested(CardDispatchAttributesSchema)
    dispatch_status = fields.String(required=False, allow_none=False)
