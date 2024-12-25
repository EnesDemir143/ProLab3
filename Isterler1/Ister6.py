class Ister6:

    @staticmethod
    def en_cok_isbirligi_yapan_yazari_bul(graph):

        en_fazla_isbirligi = 0
        en_cok_isbirligi_yapan_yazar = None

        for yazar, ortak_yazarlar in graph.items():
            ortak_yazar_sayisi = len(ortak_yazarlar)

            if ortak_yazar_sayisi > en_fazla_isbirligi:
                en_fazla_isbirligi = ortak_yazar_sayisi
                en_cok_isbirligi_yapan_yazar = yazar

        return (en_cok_isbirligi_yapan_yazar, en_fazla_isbirligi)

