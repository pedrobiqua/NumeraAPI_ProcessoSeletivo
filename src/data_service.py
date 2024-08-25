import xmltodict
import requests
from .model.database import processar_e_inserir_dados, select_all_data

class DataSystem:
    """
    Classe abstrata para tratar dados dos subsystemas
    """
    def __init__(self) -> None:
        self.result_api = []

    def normalize_data(self, standardized_data):
        
        questions = []
        answers = []

        qa_dict = {}

        if standardized_data is not None:
            if standardized_data["survey_id"] == 1:
                
                for i in standardized_data["answers"]:
                    for _, inner_dict in i["survey_data"].items():
                        questions.append(inner_dict["question"])
                        if "answer" in inner_dict:
                            answers.append(inner_dict["answer"])
                        else:
                            answers.append("Empty answer")
                
            elif standardized_data["survey_id"] == 2:
                # Formatação de 2
                for i in standardized_data["answers"]:
                    for key, value in i.items():
                        if len(str(key)) > 20:
                            questions.append(key)
                            if value is not "":
                                answers.append(value)
                            else:
                                answers.append("Empty answer")

            elif standardized_data["survey_id"] == 3:
                for i in standardized_data["answers"]["item"]:
                    for key, value in enumerate(i["survey_data"]["item"]):
                        questions.append(value["question"])
                        if "answer" in value:
                            answers.append(value["answer"])
                        else:
                            answers.append("Empty answer")

            
            # Normaliza os dados para o retorno
            for questions, answers in zip(questions, answers):
                if questions in qa_dict:
                    qa_dict[questions].append(answers)
                else:
                    qa_dict[questions] = [answers]

            # qa_dict["survey_id"] = standardized_data["survey_id"]
            return qa_dict

class Subsystem1(DataSystem):
    """
    Subsystem1 interacts with the first API.
    """

    def fetch_data(self) -> dict | None:
        response = requests.get("https://numera-case.web.app/v1/survey/1/answers")
        data = response.json()
        # Here you would standardize the data
        standardized_data = {
            "survey_id": 1,
            "answers": data["data"]
        }
        
        normalized = self.normalize_data(standardized_data)

        return normalized


class Subsystem2(DataSystem):
    """
    Subsystem2 interacts with the second API.
    """

    def fetch_data(self) -> dict | None:
        response = requests.get("https://numera-case.web.app/v1/survey/2/answers")
        data = response.json()
        # Standardize the data
        standardized_data = {
            "survey_id": 2,
            "answers": data["data"]
        }

        normalized = self.normalize_data(standardized_data)
        return normalized


class Subsystem3(DataSystem):
    """
    Subsystem3 interacts with the third API.
    """

    def fetch_data(self) -> dict | None:
        response = requests.get("https://numera-case.web.app/v1/survey/3/answers")
        if 'application/xml' in response.headers['Content-Type']:
            data = xmltodict.parse(response.text)
            standardized_data = {
                "survey_id": 3,
                "answers": data["survey_answer"]["data"]
            }
            normalized = self.normalize_data(standardized_data)
            return normalized
        else:
            data = response.json()
            # Standardize the data
            standardized_data = {
                "survey_id": 3,
                "answers": data["data"]
            }
        return standardized_data

class Facade:
    """
    The Facade class provides a simple interface to interact with different
    survey APIs and stores the results in a centralized 'database'.
    """

    def __init__(self, subsystem1: Subsystem1, subsystem2: Subsystem2, subsystem3: Subsystem3) -> None:
        """
        Initializes the facade with the provided subsystems or creates new ones.
        """
        self._subsystem1 = subsystem1 or Subsystem1()
        self._subsystem2 = subsystem2 or Subsystem2()
        self._subsystem3 = subsystem3 or Subsystem3()
        self._database = []

    def operation(self) -> None:
        """
        The Facade's operation method fetches data from the subsystems and
        stores it in the 'database'.
        """
        print("Facade initializes subsystems and collects data:")
        
        data = self._subsystem1.fetch_data()
        processar_e_inserir_dados(data, "survey_1")

        data = self._subsystem2.fetch_data()
        processar_e_inserir_dados(data, "survey_2")

        data = self._subsystem3.fetch_data()
        processar_e_inserir_dados(data, "survey_3")

        print("Data collected and stored in the database.")

    def get_database(self) -> list:
        """
        Returns the stored data from the 'database'.
        """
        # Fazer select dos dados
        data = select_all_data()
        return data
