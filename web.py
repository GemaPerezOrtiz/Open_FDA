#MIT License

#Copyright (c) [2017] [GEMA PEREZ ORTIZ]

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#primera parte montar servidor
import http.server
import http.client
import json
import socketserver

'search=patient.drugs.medicinalproduct:"LYRICA"'+'&limit=10'

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"

    def get_companies(self,drug):
        connection = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        connection.request("GET",self.OPENFDA_API_EVENT +'?search=patient.drug.medicinalproduct:'+drug+'&limit=10')
        r1 = connection.getresponse()
        data1 = r1.read() #te devuelve la informacion en bytes
        data1 = data1.decode("utf8") #para pasar de bytes a string
        event = data1

        return event

    def get_medical_product(self,companumero): #sacar el evento bien!!!!!!!!!!!!****
        connection = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        connection.request("GET",self.OPENFDA_API_EVENT +'?search=companynumb:'+companumero+'&limit=10')
        r1 = connection.getresponse()
        data1 = r1.read() #te devuelve la informacion en bytes
        data1 = data1.decode("utf8") #para pasar de bytes a string
        event = data1

        return event

    def get_event(self):
        connection = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        connection.request("GET",self.OPENFDA_API_EVENT + "?limit=10")
        r1 = connection.getresponse()
        data1 = r1.read() #te devuelve la informacion en bytes
        data1 = data1.decode("utf8") #para pasar de bytes a string
        event = data1

        return event

    def main_page(self):
        html = '''
        <html>
            <head>
                <title>OpenFDA ingenieros chulos</title>
            </head>
            <body>
            <h1>OPEN FDA client</>
            <form method="get" action="receive">
                    <input type="submit" value="listDrugs">
                    </input>
                </form>
                <form method="get" action="search">
                    </input>
                    <input type="submit" value="Drug search LYRICA">
                    </input>
                    </form>
                <form method="get" action="search">
                    medicamento: <input type="text" name="Drug"></input>
                    <input type="submit" value="Search companynumb"></input>
                    </form>
                <form method="get" action="search">
                    companynumb: <input type="text" name="companynumb"></input>
                    <input type="submit" value="Search medical product"></input>
                    </form>
            </body>
        </html>
        '''

        return html

    def find_path(self):
        return print(self.path)

    def do_head(self):
        # Send response status code
        self.send_response(200)#respuesta de que todo va bien, el self es el handler
        # Send headers
        self.send_header("Content-type","text/html") #va a devolver contenidos en http
        self.end_headers()

        return


    def send_ans(self,html):
        if self.path == '/':
            return self.wfile.write(bytes(html, "utf8")) #fichero de escritura que llega al cliente
        elif self.path=='/receive':
            event=self.get_event()
            list_drugs=self.get_list(event)
            html=self.html_event(list_drugs)
        elif self.path == '/search':
            drug = "LYRICA"
            event =self.get_companies(drug)
            list_companies=self.get_companies_list(event)
            html= self.html_event(list_companies)
        elif '/search?Drug' in self.path:
            drug = self.path.split("=")[1]
            event = self.get_companies(drug)
            list_companies=self.get_companies_list(event)
            html=self.html_event(list_companies)
        elif '/search?companynumb' in self.path:
            number = self.path.split("=")[1]
            event = self.get_medical_product(number)
            list_numbers=self.get_list(event)
            html = self.html_event(list_numbers)
        else:
            return self.wfile.write(bytes('Nanay',"utf8"))

        return self.wfile.write(bytes(html, "utf8"))



    # GET, metodo GET
    def do_GET(self): #en self controlamos la orden
        self.do_head()
        # Send message back to client
        html = self.main_page()
        # Write content as utf-8 data
        self.send_ans(html)
        return

    def get_list(self,event):
        drug=[]
        #event = self.get_event()
        event1 = json.loads(event)
        results = event1['results']
        for i in results:
            drug+= [i["patient"]["drug"][0]["medicinalproduct"]]
        return drug

    def get_companies_list(self,event):
        company=[]
        #event = self.get_companies(DRUG)
        event1 = json.loads(event)
        results = event1["results"]
        for comp in results:
            company += [comp["companynumb"]]

        return company

#---------------HTML

    def html_event(self,items_list):
        s=''
        for item in items_list:
            s += "<li>"+item+"</li>"
        html='''
        <html>
            <head></head>
                <body>
                    <ul>
                        %s
                    </ul>
                </body>
        </html>''' %(s)
        return html
