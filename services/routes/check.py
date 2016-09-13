from flask_restful import reqparse
from flask_restful import Resource
from flask import  jsonify, abort, make_response, request, g
import MySQLdb
import collections
import logging

from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from jsonschema import validate


class CardCheckReport(Resource):
    def get(self):
        logger = logging.getLogger("CardCheckReport")
        logger.info('Entered into CardCheckReport get  method')

        try:
            cursor = g.appdb.cursor()
            store_id = request.args.get("store_id")
            reported_date = str(request.args.get("reported_date"))
            employee_initials = str(request.args.get("employee_initials"))
            reported_time = str(request.args.get("reported_time"))

        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """ SELECT CAST(reported_time as char) AS time FROM card_reader_report where store_id = %s and reported_date = %s """
        cursor.execute(query, (store_id, reported_date ))
        rv = cursor.fetchall()

        newID = 0
        if len(rv) == 0:
            sub_query = """ INSERT INTO card_reader_report (store_id, employee_initials, reported_date, reported_time) VALUE (%s, %s, %s, %s) """
            cursor.execute(sub_query, (store_id, employee_initials, reported_date, reported_time))
            g.appdb.commit()
            newID = cursor.lastrowid

        logger.info('Exited from the CardCheckReport Method')
        return jsonify({"status":"success","response":rv, "ID":newID})

class ItEquipmentReport(Resource):
    def get(self):
        logger = logging.getLogger("ItEquipmentReport")
        logger.info('Entered into ItEquipmentReport get  method')

        try:
            cursor = g.appdb.cursor()
            store_id = request.args.get("store_id")
            reported_date = str(request.args.get("reported_date"))
            employee_initials = str(request.args.get("employee_initials"))
            reported_time = str(request.args.get("reported_time"))

        except:
            logger.error('Database connection or url parameters error', exc_info=True)

        query = """ SELECT CAST(reported_time as char) AS time FROM it_payment_report where store_id = %s and reported_date = %s """
        cursor.execute(query, (store_id, reported_date ))
        rv = cursor.fetchall()

        newID = 0
        if len(rv) == 0:
            sub_query = """ INSERT INTO it_payment_report (store_id, employee_initials, reported_date, reported_time) VALUE (%s, %s, %s, %s) """
            cursor.execute(sub_query, (store_id, employee_initials, reported_date, reported_time))
            g.appdb.commit()
            newID = cursor.lastrowid

        logger.info('Exited from the ItEquipmentReport Method')
        return jsonify({"status":"success","response":rv, "ID":newID})
