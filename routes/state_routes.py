from fastapi import APIRouter
from controllers.state_controller import addState,getStates,deleteState
from models.state_model import State,StateOut

router = APIRouter()

@router.post("/addState/")
async def post_state(state:State):
    return await addState(state)

@router.get("/getStates/")
async def get_states():
    return await getStates()

@router.delete("/state/{stateId}")
async def delete_state(stateId:str):
    return await deleteState(stateId)