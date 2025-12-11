from typing import Annotated

from fastapi import APIRouter, status

from pydantic import BaseModel
from pydantic_extra_types import phone_numbers

from backend.db import DBSession


PhoneNumber = Annotated[
    str | phone_numbers.PhoneNumber,
    phone_numbers.PhoneNumberValidator(
        supported_regions=["RU"],
        default_region="RU",
        number_format="E164",
    ),
]

router = APIRouter(
    prefix="",
    tags=["address-book"],
)


class AddressEntryCreateIn(BaseModel):
    phone: PhoneNumber
    address: str


class AddressEntryCreateOut(BaseModel):
    phone: PhoneNumber
    address: str


class AddressEntryUpdateIn(BaseModel):
    address: str


class AddressEntryUpdateOut(BaseModel):
    phone: PhoneNumber
    address: str


class AddressEntryViewOut(BaseModel):
    phone: PhoneNumber
    address: str


@router.post(
    "/",
    summary="Добавление новой записи в телефонную книгу",
    status_code=status.HTTP_201_CREATED,
    name="address-book:create",
    response_model=AddressEntryCreateOut,
)
async def create_address_entry(
    db_session: DBSession,
    data: AddressEntryCreateIn,
):
    address = await db_session.create(data.phone, data.address)
    return {
        "phone": data.phone,
        "address": address,
    }


@router.get(
    "/{phone}",
    summary="Просмотр записи в телефонной книге",
    status_code=status.HTTP_200_OK,
    name="address-book:read",
    response_model=AddressEntryViewOut,
)
async def read_address_entry(
    db_session: DBSession,
    phone: PhoneNumber,
):
    address = await db_session.get(phone)

    return {
        "phone": phone,
        "address": address,
    }


@router.patch(
    "/{phone}",
    summary="Обновление записи в телефонной книге",
    status_code=status.HTTP_200_OK,
    name="address-book:update",
    response_model=AddressEntryUpdateOut,
)
async def update_address_entry(
    db_session: DBSession,
    phone: PhoneNumber,
    data: AddressEntryUpdateIn,
):
    address = await db_session.update(phone=phone, address=data.address)
    return {
        "phone": phone,
        "address": address,
    }


@router.delete(
    "/{phone}",
    summary="Удаление записи из телефонной книги",
    status_code=status.HTTP_204_NO_CONTENT,
    name="address-book:delete",
)
async def dalete_address_entry(
    db_session: DBSession,
    phone: PhoneNumber,
):
    await db_session.delete(phone)
