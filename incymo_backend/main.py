from typing import Dict, List

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

from incymo_backend.enums import OfferReactionType
from incymo_backend.experiments import TestExperiment

app = FastAPI()

@app.get("/live", include_in_schema=False)
async def liveness_probe():
    """Kubernetes liveness probe."""
    return {"status": "OK"}


api_v1 = APIRouter(prefix="/v1")


@api_v1.get("/test-experiment/")
async def get_experiment(api_key: str, user_id: str) -> Dict:
    """Test endpoint for receiving a result a test experiment."""
    exp = TestExperiment(userid=user_id)
    result = {
        "assignment": {
            "inputs": exp.inputs,
            "output_data": exp.get_params(),
        },
        "debug_info": exp,
    }

    return result


@api_v1.get("/get-treatment")
async def get_treatment(api_key: str, user_id: str) -> List[str]:
    """Receiving request about treatment for processing from game client."""
    return ["TEST1", "TEST2"]


@api_v1.get("/get-offer")
async def get_offer(api_key: str, user_id: str, marker_id: str):
    """Receiving a request from game client about getting our offer.

    Structure a request:

    message GetOfferRequest {
        required string api_key = 1;
        string user_id = 2;
        string marker_id = 3;
    }

    This is endpoint will sending response with this structure:

    message GetOfferReply {
        string offer_id = 1;
        //offer structure
    }
    """

    return {"item": "sword"}


class OfferReaction(BaseModel):
    """The structure of offer for user."""

    reaction: OfferReactionType
    api_key: str
    offer_id: str
    price: float


@api_v1.post("/collect-offer-response")
async def collect_offer_response(offer_response: OfferReaction):
    """Collect the offers that the user has chosen in the game.

    This is endpoint will sending response with this structure:

        message CollectOfferResponseRequest {
            enum OfferResponse {
                UNKNOWN = 0;
                CLICK_PURCHASE = 1;
                CLICK_NO_PURCHASE = 2;
                DISMISS = 3;
                IGNORE = 4;
            }
            required string api_key = 1;
            string offer_id = 3;
            //purchase sum, item?
        }
    """

    return offer_response


app.include_router(api_v1)

def start():
    print('Hello')
    