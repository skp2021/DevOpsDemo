from flask import Flask, jsonify
from kubernetes import client, config
from flaskext.mysql import MySQL
import os

if os.getenv('KUBERNETES_SERVICE_HOST'):
    config.load_incluster_config()
v1 = client.CoreV1Api()
my_app = Flask(__name__)


my_app.config["MYSQL_DATABASE_USER"] = "root"
my_app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
my_app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
my_app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
my_app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))

mysql = MySQL()
mysql.init_app(my_app)


namespaces_information = []
@my_app.route("/")


def ns_info():
        ns_list = v1.list_namespace()
        print("####################################################")
        print("Printing only the names of the namespaces")
        print("####################################################")
        for item in ns_list.items:
            namespaces_information.append("%s" % (item.metadata.name))
        return jsonify(namespaces_information)


pod_information = []
@my_app.route("/pod")


def pod_info():
        describe_pods = v1.list_pod_for_all_namespaces()
        print("##################################################")
        print("Printing selective information about pods")
        print("##################################################")
        for item in describe_pods.items:
                pod_information.append(
                            " %s   %s" %
                            (item.metadata.namespace,
                             item.metadata.name))
        return jsonify(pod_information)

conn = mysql.connect()
cursor = conn.cursor()


for item in namespaces_information:
    temp = item[1]
    sql = "INSERT INTO namespaces (NAMESPACE) VALUES (%s);"
    cursor.execute(sql, temp)
    conn.commit()
for obj in pod_information:
    var1 = obj[1]
    var2 = obj[2]
    sql1 = "INSERT INTO pods (NAMESPACE, POD_NAME) VALUES (%s, %s);"
    cursor.execute(sql1, var1, var2)
    conn.commit()

cursor.close()
conn.close()

if __name__ == "__main__":
    my_app.run(debug=True, host='0.0.0.0', port=5000)
