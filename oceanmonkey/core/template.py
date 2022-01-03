import abc
import os
import string
import oceanmonkey

class Template(abc.ABC):
    @abc.abstractmethod
    def create(self):
        """ """

class ProjectTemplate(Template):
    def __init__(self, project_name):
        self.__project_name = project_name
        self.__project_template_path = os.path.join(
            os.path.dirname(oceanmonkey.__file__), "templates", "project"
        )
        self.__monkeys_template_path = os.path.join(
            os.path.dirname(oceanmonkey.__file__), "templates", "monkeys"
        )

    def create(self, monkey_name="WuKong"):
        clean_project_name = os.path.basename(self.__project_name)
        template_args = {"project_name": clean_project_name}
        os.makedirs(os.path.join(self.__project_name, clean_project_name))
        for root, dirs, files in os.walk(self.__project_template_path, topdown=False):
            for name in files:
                if not name.endswith(".cfg") and not name.endswith(".tmpl"):
                    continue
                file_name = os.path.join(root, name)
                template = string.Template(open(file_name, "r").read())
                template = template.substitute(template_args)
                if file_name.endswith(".cfg"):
                    with open(os.path.join(self.__project_name, "oceanmonkey.cfg"), "w") as f:
                        f.write(template)
                elif file_name.endswith(".tmpl"):
                    basename = os.path.basename(file_name)
                    python_file_name = basename[:basename.find(".tmpl")]
                    with open(os.path.join(self.__project_name, clean_project_name,
                                           python_file_name), "w") as f:
                        f.write(template)

        monkeys = "monkeys"
        template_args = {"monkey_name": monkey_name}
        os.makedirs(os.path.join(self.__project_name, clean_project_name, monkeys))

        for root, dirs, files in os.walk(self.__monkeys_template_path, topdown=False):
            for name in files:
                if not name.endswith(".tmpl"):
                    continue
                file_name = os.path.join(root, name)
                template = string.Template(open(file_name, "r").read())
                template = template.substitute(template_args)
                basename = os.path.basename(file_name)
                python_file = basename[:basename.find(".tmpl")]
                with open(os.path.join(self.__project_name, clean_project_name,monkeys,
                                       python_file), "w") as f:
                    f.write(template)


