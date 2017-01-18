# yandex-traffic
Rest api for yandex traffic (time in way between points in traffic conditions)

## Api examples:
- /report/text/55.67,37.76;55.79,37.66 - get text report
- /report/json/55.67,37.76;55.79,37.66 - get json report

Text response:
```
Время в пути: 40 мин
Краснодарская улица - 2 мин (расстояние: 840 м; скорость: 18 км\ч)
Краснодонская улица - 3 мин (расстояние: 2 км; скорость: 27 км\ч)
Волжский бульвар - 4 мин (расстояние: 1,6 км; скорость: 27 км\ч)
Волгоградский проспект (дублёр) - 2 мин (расстояние: 800 м; скорость: 35 км\ч)
Волгоградский проспект - 3 мин (расстояние: 2,1 км; скорость: 57 км\ч)
ТТК - 49 сек (расстояние: 641,3 м; скорость: 27 км\ч)
-----------------------------
Время в пути: 43 мин
Краснодарская улица - 3 мин (расстояние: 1,5 км; скорость: 19 км\ч)
Люблинская улица - 6 мин (расстояние: 4,2 км; скорость: 38 км\ч)
Остаповский проезд - 1 мин (расстояние: 1,5 км; скорость: 46 км\ч)
Волгоградский проспект - 2 мин (расстояние: 1,9 км; скорость: 36 км\ч)
Марксистская улица - 2 мин (расстояние: 1,2 км; скорость: 17 км\ч)
Садовое кольцо - 31 сек (расстояние: 88,1 м; скорость: 37 км\ч)
Каланчёвская улица - 47 сек (расстояние: 324,6 м; скорость: 20 км\ч)
Краснопрудная улица - 2 мин (расстояние: 950 м; скорость: 18 км\ч)
Гаврикова улица - 6 сек (расстояние: 30,3 м; скорость: 13 км\ч)
```
