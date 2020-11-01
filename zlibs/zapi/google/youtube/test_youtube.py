import youtube as script

import requests


class TestYoutube:

    def test_video(self):

        # assert azerty == place
        pass

    # def test_query(self):

    #     quote_lst = [
    #         "Salut GrandPy ! Est-ce que tu connais l'adresse d'{}",
    #         "Salut GrandPy ! Dis moi où se situe {}, j'aimerais bien y aller.",
    #         "Où est {} ?",
    #         "Où se trouve {}.",
    #         "Je cherche l'adresse de {}",
    #         "Je cherche {}",
    #         "Je cherche {}. Sais-tu où ça se trouve ?",
    #         "Aller à {}",
    #         "Aller au {}",
    #         "Aller chez {}",
    #         "Aller en {}",
    #         "Tu connais cette adresse: {} ?",
    #         "connais-tu ce lieu {} ?",
    #         "Connais-tu cet endroit {} ?, je cherche à y aller.",
    #         "connais-tu ce coin {} ? Je dois aller chez eux",
    #         # "connais-tu ce spot {} ?, Ca m'a l'air assez chouette.",
    #         "J'ai rendez-vous au {} et je cherche cette adresse",
    #         "J'ai rdv au {} et je cherche cette adresse",
    #         "Aller en {}",
    #         "{} sais-tu où ça se trouve ?",
    #         "{} sais-tu comment y aller ?",
    #         "{}"
    #         ]

    #     place_lst = [
    #         "Paris",
    #         "Cité la Meynard",
    #         "OpenClassrooms",
    #         "Prades-le-Lez",
    #         "Rue Alexandra David Neel, Pradres-le-Lez",
    #         "Place de la comédie",
    #         "Somfy, Cluses",
    #         ""
    #     ]

    #     # place_lst = [
    #     #     "Paris",
    #     #     "Samoëns",
    #     #     "Cluses",
    #     #     "Cité la Meynard",
    #     #     "OpenClassrooms",
    #     #     "Prades-le-Lez",
    #     #     "Rue Alexandra David Neel, Pradres-le-Lez",
    #     #     "Montpellier",
    #     #     "Comédie",
    #     #     "Place de la comédie"
    #     #     "Tour lumina",
    #     #     "Japon",
    #     #     "MIT",
    #     #     "Awox",
    #     #     "Vivaltis",
    #     #     "Somfy, Cluses",
    #     #     ""
    #     # ]

    #     for quote in quote_lst:

    #         # print("quote:", quote)

    #         for place in place_lst:
    #             # print("place:", place)
    #             qt = quote.format(place)
    #             print("quote:", qt)

    #             query = script.ZQuery(qt)

    #             # define expected place
    #             place = query.remove_punctuation(place.lower())

    #             word_lst = place.split()
    #             place = ''.join([w + " " for w in word_lst if w not in query._STOP_WORD_FR_LIST_])
    #             if place not in ["", " ", "  ", "   "]:
    #                 while place[0] == " ":
    #                     place = place[1:]
    #                 while place[-1] == " ":
    #                     place = place[:-1]

    #             assert query.spot[0] == place

    # # def test_latitude_degrees_range():
    # #     with pytest.raises(AssertionError):
    # #     position = script.Position(100, 100)



# def test_geocoding_return(monkeypatch):
    
#     geocoding_reply_dct = {'results': [{'address_components': [{'long_name': 'Cluses', 'short_name': 'Cluses', 'types': ['locality', 'political']}, {'long_name': 'Haute-Savoie', 'short_name': 'Haute-Savoie', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'Auvergne-Rhône-Alpes', 'short_name': 'Auvergne-Rhône-Alpes', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'France', 'short_name': 'FR', 'types': ['country', 'political']}, {'long_name': '74300', 'short_name': '74300', 'types': ['postal_code']}], 'formatted_address': '74300 Cluses, France', 'geometry': {'bounds': {'northeast': {'lat': 46.08459, 'lng': 6.608080999999999}, 'southwest': {'lat': 46.040365, 'lng': 6.546846899999999}}, 'location': {'lat': 46.06039, 'lng': 6.580582}, 'location_type': 'APPROXIMATE', 'viewport': {'northeast': {'lat': 46.08459, 'lng': 6.608080999999999}, 'southwest': {'lat': 46.040365, 'lng': 6.546846899999999}}}, 'place_id': 'ChIJicNpE94GjEcRuiD-B6wY98Y', 'types': ['locality', 'political']}], 'status': 'OK'}
#     result_dct = {'address': '74300 Cluses, France', 'location': {'lat': 46.06039, 'lng': 6.580582}}

#     class ResponseMocked:

#         def __init__(self, status_code, data):
#             self.status_code = status_code
#             self.data = data

#         def json(self):
#             return self.data

#     def mockreturn(url):
#         return ResponseMocked(200, geocoding_reply_dct)

#     monkeypatch.setattr(requests, 'get', mockreturn)

#     maps = script.ZGMaps(0)
#     assert maps.geocoding_request('cluses') == result_dct


# def test_geocoding_url(monkeypatch):

#     key = "azertyuiop"
#     result = "https://maps.googleapis.com/maps/api/staticmap?center=14.6332414%2C-61.03804399999999&zoom=15&size=240x240&maptype=roadmap&markers=color%3Ablue%7Clabel%3AP%7C14.6332414%2C-61.03804399999999&key={}".format(key)

#     maps = script.ZGMaps(key)

#     assert maps.static_map_request_url(14.6332414, -61.03804399999999) == result
