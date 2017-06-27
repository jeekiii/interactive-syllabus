from docutils.parsers.rst import Directive
from docutils import nodes
from werkzeug.utils import secure_filename
from flask.helpers import get_root_path
import collections
import os

import syllabus.utils.pages

from syllabus.config import *


class InginiousDirective(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    html = """
    <div class="inginious-task" style="margin: 20px">
        <div class="feedback-container" class="alert alert-success" style="padding: 10px;" hidden>
            <strong>Success!</strong> Indicates a successful or positive action.
        </div>
        <form method="post" action="http://{0}:{1}/{2}">
            <textarea style="width:100%; height:150px;" class="inginious-code" name="code">{3}</textarea><br/>
            <input type="text" name="taskid" class="taskid" value="{4}" hidden/>
            <input type="text" name="input" class="to-submit" hidden/>
        </form>
        <button class="btn btn-primary button-inginious-task" id="{4}" value="Submit">Submit</button>
    </div>

    """

    def run(self):
        par = nodes.raw('', self.html.format(inginious_instance_hostname, inginious_instance_port,
                                             inginious_instance_course_id, '\n'.join(self.content),
                                             self.arguments[0]), format='html')
        return [par]


class ToCDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    html = """
    <div id="table-of-contents">
        <h2> Table des matières </h2>
    """

    #def run(self):
        # if len(self.arguments) == 0:
        #     tmp = "<ol>\n"
        #     for line in self.content:
        #         splitted = line.split("|")
        #         if len(splitted) == 2:
        #             tmp += '<li style="list-style-type: none;"><a href=' + splitted[1] + '>' + splitted[0] + '</a></li>\n'
        #         else:
        #             tmp += '<li style="list-style-type: none;"><a href=' + line + '>' + self.getName("pages/"+splitted[0]) + '</a></li>\n'
        #     tmp += "</ol>"
        #     return [nodes.raw(' ', tmp, format='html')]
        #
        # toc = syllabus.utils.pages.get_syllabus_toc(self.arguments[0])
        # self.html += self.parse(toc[self.arguments[0]], "")
        # self.html += "</div>"
        # return [nodes.raw(' ', self.html, format='html')]

    def run(self):
        toc = syllabus.get_toc()
        for keys in toc.keys():
            self.html += "<h3> " + toc[keys]["title"] + "</h3>\n"
            self.html += self.parse(toc[keys]["content"], keys + "/")
        return [nodes.raw(' ',self.html,format='html')]

    def parse(self, dictio, pathTo):
        tmp_html = "<ul>\n"
        for key in dictio:
            tmp_html += '<li style="list-style-type: none;"><a href=' + pathTo +key + '>' + dictio[key]["title"] + '</a></li>\n'
            if "content" in dictio[key]:
                tmp_html += self.parse(dictio[key]["content"],pathTo+key+"/")
        tmp_html += "</ul>"
        return tmp_html
