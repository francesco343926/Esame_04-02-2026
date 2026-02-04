from database.DB_connect import DBConnect
from model.artist import Artist
class DAO:

    @staticmethod
    def getruoli():      #[ruolo-str]
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.role
from authorship a"""
        cursor.execute(query)

        for row in cursor:
            result.append(row['role'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getnodes(ruolo) :       #{idartist-int --> obj-artist}
        conn = DBConnect.get_connection()
        result = dict()
        cursor = conn.cursor(dictionary=True)
        query = """select a.artist_id, a.name, COUNT(o.object_id) as indice
from artists a , authorship at, objects o
where a.artist_id = at.artist_id 
	and at.role= %s
	and at.object_id = o.object_id 
	
group by a.artist_id"""
        cursor.execute(query, (ruolo,))

        for row in cursor:
            a= Artist(id=row['artist_id'], name=row['name'],
                      indice =row['indice'])
            result[a.id]= a

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getedges(ruolo):      #{(idartist1-int, idartist2-int) --> peso-float}
        conn = DBConnect.get_connection()
        result = dict()
        cursor = conn.cursor(dictionary=True)
        query = """select distinct at.artist_id
from  authorship at, objects o
where at.object_id= o.object_id
	and o.curator_approved= 1
	and at.role = %s
                
                """
        cursor.execute(query, (ruolo,))

        listaid_corretti= []
        for row in cursor:
            listaid_corretti.append(row['artist_id'])

        for id1 in listaid_corretti:
            for id2 in listaid_corretti:
                if id1 != id2:
                    if (id1, id2) not in result:
                        result[(id1, id2)]= 0


        cursor.close()
        conn.close()
        return result

