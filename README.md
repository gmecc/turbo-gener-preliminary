# Программа расчета оптимальной частоты вращения турбогенератора

Программа построена на основе методики предварительного расчета высокооборотных турбогенераторов с радиально-осевой турбиной с целью определения их оптимальных характеристик на этапе их предварительного проектирования [1].

### Оптимальные характеристики радиально-осевой турбины

Методика предварительного расчета основана на определении характеристик радиально-осевой турбины с использованием критерия подобия – коэффициента быстроходности.

Для описания условий работы турбомашин используют коэффициент быстроходности, поскольку он объединяет частоту вращения вала, объемный расход рабочего тела и располагаемую удельную работу

$$
n_s={\omega \sqrt{G_{V2}}\over (\Delta h_{0.2s})^{3/4}}
$$

где
- $\omega$ - круговая частота вращения ротора турбины;
- $\Delta h_{0.2s}$ перепад энтальпий при изоэнтропическом расширении рабочего тела в турбине по параметрам торможения;
- $G_{V2}$ - объемный расход рабочего тела на выходе из турбины

Для математического описания данных зависимостей, которые связывают КПД и коэффициент скорости с коэффициентом быстроходности, Балье и др. [2] предложены уравнения, для коэффициента скорости

$$
\nu=0.737 n_s^{0.2}
$$

для КПД

$$
\eta_e=0.87-1.07(n_s-0.55)^2-0.5(n_s-0.55)^3
$$

График зависимостей коэффициента скорости $\nu$ и КПД $\eta_e$ показан на рисунке.
![ ](balje.png)

Из графика видно, что максимальному значению КПД сосответствует значение коэффициента быстроходности

$$
n_s|_{\eta_e max}=0.543
$$


### Предварительный расчет характеристик электрического генератора

Технико-экономические показатели, размеры, масса и стоимость электрической машины зависят от ее главных размеров — внутреннего диаметра сердечника якоря  $𝐷$ и расчетной длины сердечника якоря $L$. В свою очередь главные размер  $𝐷$   решающим образом зависит от основных электромагнитных нагрузок машины — индукции в воздушном зазоре $B$ и линейной нагрузки  $𝐴$   в номинальном режиме.

Для определения главных размеров генераторов переменного тока пользуются известным выражением для машинной постоянной Арнольда [3]:

$$
C_A={D^2 \cdot L \cdot n \over k_e \cdot P_н} =
{6.1 \cdot 10^7 \over \alpha_{\delta} \cdot k_B \cdot k_{\omega} \cdot A \cdot B_\delta}
$$

где
- $С_А$ – машинная постоянная Арнольда;
- $D$ – диаметр расточки статора (см);
- $L$ – расчетная длина статора (см);
- $P_н$ – номинальная мощность генератора (кВА);
- $k_e$ – коэффициент учитывающий внутреннее падение напряжения в генераторе;
- $\alpha_{\delta}$ – расчетный коэффициент полюсного перекрытия;
- $k_B$ - коэффициент формы поля;
- $k_{\omega}$ – обмоточный коэффициент;
- $А$ – линейная нагрузка (А/см);
- $B_{\delta}$ – индукция в зазоре (Тл).

Диаметр расточки статора

$$
D={v \over \pi n}+2\delta
$$

где $v$ - окружная скорость ротора, $\delta$ - магнитный зазор.

Допустимая окружная скорость по диаметру ротора:
- 100...120 м/с - для металлической оболочки;
- 150 м/с - для металлической оболочки с высоким КП;
- до 210 м/с - для композитной оболочки

Таким образом, при известной величине машинной постоянной Арнольда м
мощность генератора

$$  P_n = \frac{2\pi n D^2 L}{k_e C_A}   $$

### Расчет

```python
from turboGenOptim import TurboGenOptim

tu = TurboGenOptim(pit=3, T_in=1250) # создание экземпляра класса turbo
tu.turbogenerator(pwr=1e5)
tu.plot(pwr=(20000, 200000))

print(f'Частота вращения турбины оптимальная {tu.n_opt_turbo*60:.0f} об/мин')
print(f'Постоянная Арнольда {tu.k_arnold:.3f} dB')
```


1. Беседин С.Н. О выборе оптимальных частот вращения турбогенерато-ров микротурбинных установок / С.Н. Беседин, В.В. Барсков, В.А. Рассохин, Н.Н. Кортиков, А.И. Рыбников // Газовая промышленность. 2024. № 3 – С. 98-105.
1. Balje O. E. Turbomachines, A Guide to Design, Selection and Theory, Wiley, New York. – 1981.
1.	Хуторецкий Г.М. Проектирование турбогенераторов / Г.М. Хуторецкий, М.И. Токов, Е.В. Толвинская // Л.: Энергоатомиздат. – 1987. – 256 с.
