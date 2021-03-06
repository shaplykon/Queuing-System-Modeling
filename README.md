### Queuing System Modeling
Лабораторная работа по предмету **"Математическое моделирование"**. 

Консольное приложение позволяет моделировать систему массового обслуживания с заданными параметрами с помощью библиотеки **SimPy**.
Результатом работы приложения является проверка модели на соответствие требованиям путём сравнения эмпирических и теоретических характеристик. 

Для построения графиков и вычисления эмпирических характеристик для каждого набора параметров симуляция производится с разным значением длительности симуляции
(5, 10, 50, 100, 500, 1000, 2000, 5000, 10000 ед. времени). Для анализа зависимости времени нахождения заявки в очереди от интенсивности потока каждый набор параметров 
тестируется на протяжении 10000 мин.(здесь минуты - единицы измерения длительности симуляции в библиотеке SimPy) с изменением параметра λ от 1 до 10.

:white_check_mark: **Анализ зависимости эмпирических характеристик от времени симуляции:**
![](https://raw.githubusercontent.com/shaplykon/Queuing-System-Modeling/master/output/images/1_test_time_dependence.png)


:white_check_mark: **Анализ зависимости времени нахождения заявки в очереди от интенсивности потока:**
![](https://raw.githubusercontent.com/shaplykon/Queuing-System-Modeling/master/output/images/1_test_queue_lambda_dependence.png)

:white_check_mark: **Индивидуальное задание.**
В качестве индивидуального задания была смоделирована одноканальная СМО с ограниченной длиной очереди. Поток заявок - простейший, 
время обслуживания распределено по обобщённому **закону Эрланга**. В рамках симуляции проведён анализ зависимости эмпирических характеристик 
от значение коэффицента Эрланга(K):
![](https://raw.githubusercontent.com/shaplykon/Queuing-System-Modeling/master/output/images/individual_test_erlang_dependence.png)
