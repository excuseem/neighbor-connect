from concurrent import futures
import grpc

import main_pb2
import main_pb2_grpc
from models import User, db_session


class UserService(main_pb2_grpc.UserService):
    def CreateProfile(self, request, context):
        user = User(request.fullname, request.telephone, request.email,
                    request.country, request.city, request.street,
                    request.bio, request.profile_picture)
        db_session.add(user)
        db_session.commit()
        return main_pb2.CreateProfileResponse(message='User Created Successfully')

    def Authenticate(self, request, context):
        user = User.query.filter_by(email=request.email).first()
        if user and user.check_password(request.password):
            return main_pb2.AuthenticateResponse(status='Logged In')
        else:
            return main_pb2.AuthenticateResponse(status='Error')

    def CreateOffer(self, request, context):
        user = db_session.query(User).get(request.user_id)
        if not user:
            return main_pb2.CreateOfferResponse(message='User not found')

        offer = Offer(
            user_id=request.user_id,
            place=request.place,
            offer=request.offer,
            tags=[Tag(tag=t) for t in request.tags]
        )
        db_session.add(offer)
        db_session.commit()

        return main_pb2.CreateOfferResponse(message='Offer Created Successfully')

    def GetOffers(self, request, context):
        offers = db_session.query(Offer).all()

        return main_pb2.GetOffersResponse(
            offers=[main_pb2.Offer(
                id=offer.id,
                user_id=offer.user_id,
                place=offer.place,
                offer=offer.offer,
                tags=[tag.tag for tag in offer.tags]
            ) for offer in offers]
        )

    def CreateIncident(self, request, context):
        user = db_session.query(User).get(request.user_id)
        if not user:
            return main_pb2.CreateIncidentResponse(message='User not found')

        incident = Incident(
            user_id=request.user_id,
            description=request.description,
            address=request.address,
            picture=request.picture
        )
        db_session.add(incident)
        db_session.commit()

        return main_pb2.CreateIncidentResponse(message='Incident Created Successfully')

    def GetIncidents(self, request, context):
        incidents = db_session.query(Incident).all()

        return main_pb2.GetIncidentsResponse(
            incidents=[main_pb2.Incident(
                id=incident.id,
                user_id=incident.user_id,
                description=incident.description,
                address=incident.address,
                picture=incident.picture
            ) for incident in incidents]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    main_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
