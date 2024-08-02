from database.DB_connect import DBConnect
from model.earthquake import Earthquake


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getLuoghi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select e.place as p
                from earthquakes e """
        cursor.execute(query)
        for row in cursor:
            if row['p'] != "":
                r = row["p"].split(",")[-1].strip()
                result.append(r)
        cursor.close()
        conn.close()
        rTemp = set(result)
        rFin = sorted(rTemp)
        return rFin

    @staticmethod
    def getTerremoti(mese):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                FROM earthquakes e 
                where e.`time` LIKE %s"""
        cursor.execute(query,(mese,))
        for row in cursor:
            result.append(Earthquake(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTerremotiZona(zona, mese):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM earthquakes e
                    WHERE e.place LIKE %s
                    and e.`time` LIKE %s"""
        cursor.execute(query, (zona,mese))
        for row in cursor:
            result.append(Earthquake(**row))
        cursor.close()
        conn.close()
        return result
