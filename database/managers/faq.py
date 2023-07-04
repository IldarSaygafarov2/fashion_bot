from .base import Manager


class FAQManager(Manager):
    def insert_test_question_answer(self) -> None:
        sql = """
            INSERT INTO faq(question, answer)
            VALUES 
            ('Есть ли у вас парковка?', 'Да, рядом с любым из наших салонов есть возможность парковки.'),
            ('Входит ли мытье волос в стоимость стрижки?', 'Да, в стоимость стрижки входит мытьё волос и укладка по форме.'),
            ('Какой эффект от процедуры ламинирования?', 'Каждый волосок обволакивается блестящей пленкой, становится толще, приобретает здоровый вид и живой блеск. Эта процедура эффективна как сама по себе, так и в дополнении к предварительному окрашиванию и к лечению волос. При нанесении ламинирования после окрашивания значительно ;продлевается; жизнь цвета волос. Цвет будет намного дольше оставаться сочным, так как сначала будет смываться ламинирование, а затем цвет. При нанесении ламинирования после лечения в волос активные вещества ;запечатываются; в чешуйках и, тем самым продлеваем действие маски.'),
            ('Чем отличается воск от шугаринга?', 'Отличий много, основное – технология. При депиляции волоски удаляются против роста волос, при шугаринге – по росту волос');
        """
        self.manager(sql, commit=True)

    def get_all_questions(self) -> list[tuple]:
        sql = """
            SELECT * FROM faq;
        """
        return self.manager(sql, fetchall=True)

    def insert_question_answer(self, question: str, answer: str) -> None:
        sql = "INSERT INTO faq(question, answer) VALUES (?,?);"
        self.manager(sql, question, answer, commit=True)

    def get_faq_id(self, faq_question: str) -> int:
        sql = "SELECT faq_id FROM faq WHERE question = ?"
        return self.manager(sql, faq_question, fetchone=True)[0]

    def delete_faq_question_answer(self, faq_id: int) -> None:
        sql = "DELETE FROM faq WHERE faq_id = ?;"
        self.manager(sql, faq_id, commit=True)

    def update_question(self, faq_id: int, new_question: str) -> None:
        sql = "UPDATE faq SET question = ? WHERE faq_id = ?"
        self.manager(sql, new_question, faq_id, commit=True)

    def update_answer(self, faq_id: int, new_answer: str) -> None:
        sql = "UPDATE faq SET answer = ? WHERE faq_id = ?"
        self.manager(sql, new_answer, faq_id, commit=True)