import pymysql
import time
import json
import os

time.sleep(1)
print("===== INTEGRATION ENGINE BANK X ONLINE SHOP =====\n")
while (1):
    try:
        connection_to_olshop = 1

        try:
            connOlshop = pymysql.connect(host='db4free.net', user='imspraktikumdama', passwd='belajaritustudy11', db='olshopdama', port=3306)
            curOlshop = connOlshop.cursor()
        except:
            print("FAILED CONNECT TO ONLINE SHOP")

        try:
            connBank = pymysql.connect(host='remotemysql.com', user='CIVh0nHZ1z', passwd='BC2nK3R6k2', db='CIVh0nHZ1z', port=3306)
            curBank = connBank.cursor()
        except:
            print("FAILED CONNECT TO BANK")

        sql_select = "SELECT * FROM tb_invoice"
        curBank.execute(sql_select)
        invoice = curBank.fetchall()

        sql_select = "SELECT * FROM tb_integrasi"
        curBank.execute(sql_select)
        integrasi = curBank.fetchall()

        print("TOTAL ROW ON INVOICE = %d || INTEGRATION = %d" % (len(invoice), len(integrasi)))

        # update listener
        if (invoice != integrasi):
            print("\n===== UPDATE DATA DETECTED =====")
            for data in invoice:
                for dataIntegrasi in integrasi:
                    if (data[0] == dataIntegrasi[0]):
                        if (data != dataIntegrasi):
                            print("----- RUN UPDATE FOR ID = %s -----\n" % (data[0]))
                            val = (data[3], data[0])
                            update_integrasi_bank = "update tb_integrasi set status_transaksi = %s where id_invoice = %s"
                            curBank.execute(update_integrasi_bank, val)
                            connBank.commit()

                            if (connection_to_olshop == 1):
                                update_integrasi_olshop = "update tb_integrasi set status_transaksi = %s where id_invoice = %s"
                                curOlshop.execute(update_integrasi_olshop, val)
                                connOlshop.commit()

                                update_invoice_olshop = "update tb_invoice set status_transaksi = %s where id_invoice = %s"
                                curOlshop.execute(update_invoice_olshop, val)
                                connOlshop.commit()

    except (pymysql.Error, pymysql.Warning) as e:
        print(e)

    # delay
    time.sleep(5)