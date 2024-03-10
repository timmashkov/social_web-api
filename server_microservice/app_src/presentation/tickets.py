from uuid import UUID

from fastapi import APIRouter, Depends

from domain.tickets.schemas import TicketOut, GetTicketId, TicketIn
from infrastructure.database.models import Ticket
from service.ticket_service import TicketService

ticket_router = APIRouter(prefix="/ticket")


@ticket_router.get("/", response_model=list[TicketOut])
async def show_tickets(
    tick_repo: TicketService = Depends(TicketService),
) -> list[Ticket]:
    return await tick_repo.get_all_tickets()


@ticket_router.get("/{ticket_id}", response_model=TicketOut)
async def show_ticket(
    ticket_id: UUID, tick_repo: TicketService = Depends(TicketService)
) -> TicketOut:
    return await tick_repo.get_ticket(cmd=GetTicketId(id=ticket_id))


@ticket_router.post("/add", response_model=TicketOut)
async def add_ticket(
    cmd: TicketIn, tick_repo: TicketService = Depends(TicketService)
) -> TicketOut:
    return await tick_repo.create_ticket(cmd=cmd)


@ticket_router.patch("/upd/{ticket_id}", response_model=TicketOut)
async def upd_ticket(
    cmd: TicketIn, ticket_id: UUID, tick_repo: TicketService = Depends(TicketService)
) -> TicketOut:
    return await tick_repo.update_ticket(cmd=cmd, data=GetTicketId(id=ticket_id))


@ticket_router.delete("/del/{ticket_id}", response_model=TicketOut)
async def del_tickets(
    ticket_id: UUID, tick_repo: TicketService = Depends(TicketService)
) -> TicketOut:
    return await tick_repo.delete_ticket(cmd=GetTicketId(id=ticket_id))
