from uuid import UUID

from fastapi import APIRouter, Depends

from domain.guests.schema import (
    GetGuestById,
    GuestOut,
    GuestIn,
    GuestUpdate,
    GuestWithTicket,
)
from infrastructure.database.models import Guest
from service import GuestService

guest_router = APIRouter(prefix="/guest")


@guest_router.get("/all", response_model=list[GuestOut])
async def show_guests(guest_repo: GuestService = Depends(GuestService)) -> list[Guest]:
    return await guest_repo.get_all_guest()


@guest_router.get("/{guest_id}", response_model=GuestOut)
async def show_guest(
    guest_id: UUID, guest_repo: GuestService = Depends(GuestService)
) -> GuestOut:
    return await guest_repo.get_guest_by_id(cmd=GetGuestById(id=guest_id))


@guest_router.get("/full/{guest_id}", response_model=GuestWithTicket)
async def show_guest_with_ticket(
    guest_id: UUID, guest_repo: GuestService = Depends(GuestService)
) -> GuestWithTicket:
    return await guest_repo.get_guest_ticket(cmd=GetGuestById(id=guest_id))


@guest_router.post("/invite", response_model=GuestOut)
async def invite_guest(
    cmd: GuestIn, guest_repo: GuestService = Depends(GuestService)
) -> GuestOut:
    return await guest_repo.add_guest(cmd=cmd)


@guest_router.patch("/upd/{guest_id}", response_model=GuestOut)
async def update_guest(
    cmd: GuestUpdate, guest_id: UUID, guest_repo: GuestService = Depends(GuestService)
) -> GuestOut:
    return await guest_repo.upd_guest(cmd=cmd, data=GetGuestById(id=guest_id))


@guest_router.delete("/del/{guest_id}", response_model=GuestOut)
async def delete_guest(
    guest_id: UUID, guest_repo: GuestService = Depends(GuestService)
) -> GuestOut:
    return await guest_repo.del_guest(cmd=GetGuestById(id=guest_id))
