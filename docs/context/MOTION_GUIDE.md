# MOTION_GUIDE.md — Dirección de movimiento y UX para la presentación scrollytelling

> **Para los 3 agentes que trabajan en la presentación.** Lean esto completo antes de tocar código.
> Este archivo es la fuente de verdad del movimiento: si algo aquí choca con su criterio, gana este archivo.
> Si encuentran un caso que no está cubierto, agréguenlo a la sección 11 (Registro de fallas) en vez de improvisar.

---

## 0. La idea en una línea

Cada adjetivo ("premium", "moderno", "wow") se convierte en un número. **Los adjetivos dan el look por defecto; los números dan el look dirigido.**
El efecto wow no viene de animar más, sino de **un solo momento coreografiado por sección**, con todo lo demás quieto o en segundo plano.

---

## 1. Contrato técnico (obligatorio)

En un scrollytelling, el tiempo `t` se reemplaza por el **progreso del scroll `p`**, de 0 a 1, en cada sección.

1. **Cada sección es una función pura del progreso.** Expone `render(p)`, que dibuja exactamente ese estado. Mismo `p`, misma imagen, siempre.
2. **El scroll solo calcula `p` y llama a `render(p)`.** GSAP ScrollTrigger, CSS scroll-driven animations (`animation-timeline: view()`) o IntersectionObserver sirven para medir. La lógica visual vive en `render(p)`, no en callbacks sueltos.
3. **Prohibido:** `Date.now()`, `setTimeout` o `setInterval` para animar, `Math.random()` sin semilla, transiciones CSS que dependan del orden de los eventos.
4. **Animar solo `transform` y `opacity`**, más `filter` y `clip-path` cuando de verdad haga falta. Nunca `width`, `height`, `top`, `left` ni `margin`: rompen los 60 fps.
5. **Librerías fijadas a una versión exacta** (por ejemplo `gsap@3.13.0`, `three@0.160.0`). Nada de `@latest`.
6. **Nada de scroll-jacking.** El usuario controla la velocidad. Se permite el smooth scroll (Lenis o similar) solo si respeta la rueda, el trackpad y el teclado, y se desactiva con `prefers-reduced-motion`.
7. **Animación ambiental en loop** (respiración, brillo lento): función pura de `t`, ciclos enteros, sin saltos en la costura.
8. **Fuentes:** `font-display: block` y esperar `document.fonts.ready` antes de medir layouts o hacer split de texto.

### Hook de congelado para QA (todas las secciones)

```js
// Abre index.html?s=hero&p=0.5 para ver la sección "hero" exactamente al 50% de su progreso.
window.__sections = window.__sections || {};   // cada sección se registra: __sections[id] = { el, render }
window.freezeAt = function (id, p) {
  const s = window.__sections[id];
  if (!s) return;
  const r = s.el.getBoundingClientRect();
  const start = window.scrollY + r.top;
  const len = s.el.offsetHeight - window.innerHeight;   // largo de scroll de la sección pinneada
  window.scrollTo(0, start + p * Math.max(len, 0));
  s.render(p);                                           // dibuja el estado exacto aunque el scroll no haya terminado
};
(function () {
  const q = new URLSearchParams(location.search);
  if (!q.has('s')) return;
  const go = () => window.freezeAt(q.get('s'), parseFloat(q.get('p')) || 0);
  document.fonts.ready.then(go);
  window.addEventListener('load', go);
})();
```

Cada sección **debe** registrarse en `window.__sections` con su `id`. Sin esto, la sección no pasa QA.

---

## 2. Tokens de movimiento (un solo archivo, sin números sueltos)

Crear **`/src/motion.js`** (y su espejo `/src/motion.css`). **Solo el Agente Líder lo edita** (ver sección 9). Los demás importan, nunca escriben valores inline.

```js
// motion.js
export const EASE = {
  enter: 'cubic-bezier(0.16, 1, 0.3, 1)',    // ease-out-expo: revelar texto y logos
  premium: 'cubic-bezier(0.22, 1, 0.36, 1)', // ease-out-quint: entradas premium
  move:  'cubic-bezier(0.76, 0, 0.24, 1)',   // ease-in-out-quart: desplazamientos y cámara
  exit:  'cubic-bezier(0.7, 0, 0.84, 0)',    // ease-in-expo: salidas rápidas
  pop:   'cubic-bezier(0.34, 1.56, 0.64, 1)' // ease-out-back: pop con overshoot (usar poco)
};
export const MS = { feedback: 150, move: 400, hero: 750, exit: 240 };
export const STAGGER = { letter: 30, word: 90, item: 60 };       // ms entre elementos
export const PARALLAX = { front: 1.0, mid: 0.5, back: 0.2 };     // velocidades relativas

// Versión JS de las curvas, para usar dentro de render(p)
const bezier = (x1, y1, x2, y2) => (x) => {
  let t = x;
  for (let i = 0; i < 8; i++) {
    const cx = 3 * x1 * t * (1 - t) ** 2 + 3 * x2 * t * t * (1 - t) + t ** 3 - x;
    const dx = 3 * x1 * (1 - t) ** 2 + 6 * (x2 - x1) * t * (1 - t) + 3 * (1 - x2) * t * t;
    if (Math.abs(dx) < 1e-6) break;
    t -= cx / dx;
  }
  return 3 * y1 * t * (1 - t) ** 2 + 3 * y2 * t * t * (1 - t) + t ** 3;
};
export const ease = {
  enter: bezier(0.16, 1, 0.3, 1),
  premium: bezier(0.22, 1, 0.36, 1),
  move: bezier(0.76, 0, 0.24, 1),
  exit: bezier(0.7, 0, 0.84, 0),
};

// Sub-rango del progreso: map(p, 0.2, 0.5) va de 0 a 1 mientras p va de 0.2 a 0.5
export const seg = (p, a, b) => Math.min(1, Math.max(0, (p - a) / (b - a)));
export const lerp = (a, b, k) => a + (b - a) * k;

// Resorte como función pura (sin simulación). zeta: 1 sin rebote, 0.8 premium, 0.5 juguetón.
export function spring(t, zeta = 0.8, f = 2) {
  if (t <= 0) return 0;
  const w = 2 * Math.PI * f;
  if (zeta >= 1) return 1 - Math.exp(-w * t) * (1 + w * t);
  const wd = w * Math.sqrt(1 - zeta * zeta);
  return 1 - Math.exp(-zeta * w * t) * (Math.cos(wd * t) + (zeta * w / wd) * Math.sin(wd * t));
}
export const dampingRatio = (k, d, m = 1) => d / (2 * Math.sqrt(k * m));

// Ruido determinista
export function rng(seed) {
  return () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
}
```

### Reglas de uso de las curvas

| Situación | Curva | Duración / largo |
|---|---|---|
| Entrada de texto o logo | `enter` | 600–900 ms, o 15–25% del scroll de la sección |
| Entrada "premium" de tarjetas o mockups | `premium` | 400–750 ms |
| Desplazamientos y movimientos de cámara | `move` | sin límite: la cámara usa la curva más suave |
| Salidas | `exit` | **40–50% más cortas que la entrada** |
| Rotaciones continuas, barras de progreso, fase de loops | lineal | — |
| Cualquier otro desplazamiento | **nunca lineal** | lineal = "se ve renderizado" |

**Resortes:** la posición y la escala pueden rebotar. **La opacidad y el color nunca rebotan.**
`zeta` 0.7–0.85 se siente premium, 0.4–0.6 juguetón, < 0.3 caricatura. Para esta presentación: **0.8 por defecto**, 0.6 solo en el momento wow de cada app.

---

## 3. Reglas de dirección para scrollytelling

### 3.1 Un protagonista por escena
- Cada escena tiene **UN movimiento protagonista**.
- Movimientos secundarios: recorren **50–70%** de la distancia del protagonista y arrancan **100–200 ms después** (en scroll: +0.05–0.1 de `p`).
- Ambientales: **< 5%** del recorrido del protagonista, en un seno lento, sin detenerse nunca.
- El siguiente elemento arranca cuando el anterior va al **30–50%**. Todo en secuencia se ve robótico; todo a la vez se ve barato.

### 3.2 El texto no se mueve mientras se lee
- El texto queda **fijo** al menos **0.3 s por palabra + 0.5 s**. En scroll: la zona de lectura debe ocupar suficiente largo de scroll (regla práctica: **≥ 40vh de scroll quieto por párrafo corto**).
- El patrón correcto: **el texto entra → queda fijo → el visual cambia a su lado → el texto sale**. Nunca texto y visual protagonista moviéndose a la vez.
- Mientras el texto está fijo, el fondo puede hacer un **push de 2%** (escala 1.00 → 1.02) para que la escena siga viva.

### 3.3 Largo de scroll por escena (presupuesto)
| Tipo de escena | Largo de scroll (pin) |
|---|---|
| Titular simple | 100–150vh |
| Narrativa con 2–3 pasos | 200–300vh (≈ 100vh por paso) |
| Momento wow de una app | 300–400vh |
| Transición entre capítulos | 50–100vh |

Si una escena se siente lenta: **acortar el pin 25%**. No acelerar las curvas.

### 3.4 Transiciones entre escenas son decisiones
Elegir una por cambio de capítulo y declararla en el brief de la escena:
- **Corte duro**: por defecto. Limpio y rápido.
- **Match cut**: una forma de la escena A se convierte en la de la escena B (por ejemplo, el ícono del problema pasa a ser el logo de la app).
- **Mask wipe**: `clip-path` que revela la siguiente escena.

Prohibido el "fade a todo" entre todas las escenas.

### 3.5 Ritmo
- Cambiar el **layout cada capítulo**, no en cada paso. Cambiar todo en cada paso agota.
- Alternar densidad: escena cargada → escena de respiro (un dato grande, una frase) → escena cargada.

### 3.6 Parallax
- Velocidades: frente 1.0, medio 0.5, fondo 0.2. **Máximo 3 capas** por escena.
- Nunca poner parallax en el texto que se está leyendo.

---

## 4. Lista de prohibidos (BANNED)

Viva: cada agente que detecte un default "de IA" lo agrega aquí.

- Degradados morados o azules, glow, orbes brillantes, lens flares, neón
- Partículas flotando como decoración
- Todo apareciendo a la vez
- **Fade + slide-up en cada elemento** (el default genérico número uno)
- Todo centrado en todas las secciones
- Texto que se mueve mientras se lee
- Glassmorphism por todas partes, bordes con gradiente animado
- Emojis como íconos
- Contadores de números que suben en cada métrica (usar solo en **un** dato hero)
- Tipografía en bloque de 5 tamaños distintos por sección (máximo 3)
- Cursor custom que persigue al mouse
- Scroll-jacking o secciones que "frenan" el scroll
- Taglines inventadas que no están en el guion
- _(agregar aquí)_

---

## 5. Brief por escena (llenar ANTES de escribir código)

Cada escena necesita este bloque en `/briefs/<id>.md`. Sin brief no hay código.

```
ID: hero | problema | app1-intro | app1-wow | app2-intro | app2-wow | cierre ...
OWNER: Agente A / B / C
GOAL: qué debe sentir o hacer el espectador, en UNA frase
PIN: largo de scroll en vh
LOOK: paleta en hex (1 acento), tipografía + peso + tamaño + tracking
HERO: el único movimiento protagonista, con sub-rango de p (ej. p 0.10→0.45, ease.enter)
SECONDARY: qué acompaña, con recorrido (50–70%) y retraso
AMBIENT: qué respira, amplitud (<5%) y período
TEXT HOLD: rango de p donde el texto queda fijo
HANDOFF: corte | match cut (qué forma) | mask wipe
BANNED extra: defaults específicos que no deben aparecer aquí
QA: capturas en p = 0, 0.25, 0.5, 0.75, 1 (desktop y móvil)
```

Si no pueden escribir GOAL en una frase, la escena no está lista para animarse.

---

## 6. Los dos teasers de las apps (el efecto wow principal)

Las apps todavía no existen, así que la empresa tiene que **verlas funcionando**. Cada app tiene una escena **"wow"** con un **product film** corto.

### Opción A: loop de video (recomendado para los momentos hero)
- 6–10 s, loop perfecto, 60 fps, hecho como HTML con `renderAt(t)` (mismo contrato que la sección 1, pero con `t`).
- Se renderiza fotograma por fotograma con Playwright y se codifica en MP4 (H.264, `yuv420p`, `-crf 18`, `+faststart`) y WebM.
- Se inserta como `<video autoplay muted loop playsinline poster="frame0.jpg">`. **El fotograma 0 debe ser una composición terminada**, porque es lo que se ve mientras carga.
- Renderizar fotogramas 0 a N-1, **nunca N** (si no, el primero se repite en la costura).
- Opcional: **scrubbear el video con el scroll** (`video.currentTime = p * duration`): el usuario "maneja" la demo. Requiere keyframes cada 1–2 fotogramas al codificar (`-g 1` o `-g 2`).

### Opción B: mockup vivo
- La pantalla de la app construida en HTML real dentro de un marco de dispositivo, animada con `render(p)`.
- Mejor para mostrar el flujo de UX paso a paso (sección 7).

### Prompt dirigido del teaser (plantilla)
```
GOAL: en 8 s el espectador entiende qué hace [APP] y siente [emoción].
OUTPUT: un HTML autocontenido, [three.js 0.160.0 | HTML+CSS], 1920x1080 (y versión 1080x1350 para móvil).
TIME: 8 s x 60 fps = 480 fotogramas, loop sí. 120 BPM: 1 beat = 30 fotogramas, los golpes caen en beats.
LOOK: [paleta hex], acento [hex] solo en [elemento], tipografía [familia, peso, tamaño, tracking].
SHOTS:
  0.0–1.0 s: [estado inicial: el problema]
  1.0–1.2 s: anticipación (contracción 2%, hold de 3 fotogramas)
  1.2 s: [el gesto clave de la app] en resorte zeta 0.6
  ...
  7.4–8.0 s: vuelta exacta al fotograma 0
CAMERA: nunca estacionada, push-in de 2% durante los holds.
BANNED: (sección 4)
QA: renderAt(t) puro, capturas alrededor de cada golpe, el fotograma 479 fluye al 0.
```

---

## 7. UX/UI de las apps: cómo mostrar que la app se *siente* bien

La presentación vende la experiencia, no solo las pantallas. Mostrar estas reglas aplicadas en los mockups:

| Interacción | Regla |
|---|---|
| Feedback de toque o clic | 100–150 ms (100 ms se siente instantáneo) |
| Movimientos de UI | 200–500 ms |
| Revelados hero (primer resultado, confirmación) | 600–900 ms |
| Listas | stagger 40–80 ms por ítem |
| Botón presionado | escala 0.97 en 100 ms, vuelve con resorte zeta 0.8 |
| "Que haga pop" | escala 1.0 → 1.08 → 1.0 en 6 fotogramas (100 ms), pico en el evento |
| Estados de carga | skeleton con brillo lineal lento, nunca spinners genéricos |
| Opacidad y color | sin rebote, nunca |

**Un momento coreografiado por app**: el instante en que la app entrega su valor (el resultado, el match, la confirmación). Ese es el único lugar donde se permite zeta 0.6 y `ease.pop`. Todo lo demás es sobrio.

---

## 8. Calidad, accesibilidad y rendimiento

- **Contraste de texto ≥ 4.5:1 en cada estado del scroll**, incluso sobre fondos en movimiento.
- **Nunca más de 3 destellos por segundo** (WCAG).
- **`prefers-reduced-motion: reduce`**: sin parallax ni scrub. Cada escena muestra su estado final (`render(1)`) o un crossfade ≤ 200 ms entre pasos. El contenido debe ser el mismo.
- 60 fps en un laptop medio: perfilar en Chrome DevTools > Performance. Sin layout shift durante el scroll.
- Texto en reposo en píxeles enteros (sin `translate` fraccionario cuando el texto está fijo). Si no, se ve borroso.
- Imágenes y videos con `width` y `height` declarados. Videos en `preload="metadata"` salvo el del hero.
- **Móvil (390x844) es ciudadano de primera clase.** Los pins duran menos (×0.7) y el layout pasa a una columna.
- La presentación debe funcionar si la empresa la abre **sin sonido**. El audio es opcional, apagado por defecto.

---

## 9. Coordinación entre los 3 agentes

### Roles sugeridos
| Agente | Dueño de | Puede editar |
|---|---|---|
| **A — Líder / sistema** | `motion.js`, `motion.css`, layout global, scroll engine, hook de QA, este archivo | Todo lo compartido. Integra. |
| **B — Narrativa** | Escenas de hero, problema, contexto y cierre | Solo `/sections/<sus-ids>/` y `/briefs/<sus-ids>.md` |
| **C — Apps** | Escenas de App 1 y App 2, teasers, mockups | Solo `/sections/app*/`, `/teasers/`, `/briefs/app*.md` |

### Reglas
1. **Nadie edita archivos de otro agente.** Si necesitas un cambio en un archivo compartido, escribe la petición en `/coord/requests.md` y la ejecuta el Agente A.
2. **Un token nuevo se pide, no se inventa.** Si una escena necesita una curva o duración que no existe, se pide al Agente A, que la agrega a `motion.js`.
3. Cada escena es un módulo independiente: `/sections/<id>/index.js` exporta `{ id, pin, render(p), mount(el) }`.
4. Registrar en `/coord/status.md`: escena, owner, estado (brief / en curso / QA / listo) y la última nota de QA.
5. Los cambios a la lista BANNED (sección 4) se pueden agregar sin pedir permiso, pero siempre al final.

---

## 10. Loop de QA: render → mirar → notas con números → arreglar

Ninguna escena se marca "lista" sin pasar este loop. Lo normal son 2–4 rondas.

### Script de capturas (Playwright)
```js
// qa-shots.mjs   uso: node qa-shots.mjs https://TU-VPS/presentacion hero,app1-wow
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';

const [url, ids = ''] = process.argv.slice(2);
const P = [0, 0.25, 0.5, 0.75, 1];
const VIEWPORTS = { desktop: { width: 1440, height: 900 }, mobile: { width: 390, height: 844 } };
const browser = await chromium.launch();
for (const [vpName, vp] of Object.entries(VIEWPORTS)) {
  const page = await browser.newPage({ viewport: vp });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  for (const id of ids.split(',').filter(Boolean)) {
    mkdirSync(`qa/${id}`, { recursive: true });
    for (const p of P) {
      await page.evaluate(([id, p]) => window.freezeAt(id, p), [id, p]);
      await page.waitForTimeout(150);
      await page.screenshot({ path: `qa/${id}/${vpName}_p${String(p).replace('.', '')}.png` });
    }
  }
  await page.close();
}
await browser.close();
```

### Notas que funcionan (siempre con escena + progreso, nunca sensaciones)
- "Captura `app1-wow` en p 0, 0.25, 0.5, 0.75 y 1. Describe cada una en una frase como la vería el cliente. ¿Coincide con el brief? Arregla lo que no."
- "En `hero`, entre p 0.3 y 0.5 se mueven 3 cosas a la vez. Deja solo el titular como protagonista; el resto arranca +0.08 de p al 60% del recorrido."
- "El texto de `problema` se mueve mientras se lee entre p 0.4 y 0.6. Fíjalo y mueve solo el visual."
- "Grafica la posición y escala del protagonista contra p. Muéstrame dónde es lineal o se detiene en seco, y arréglalo con los tokens."
- "Revisa esto como un motion designer senior: 10 notas ordenadas por impacto, cada una con escena, p y el cambio exacto de código. Aplica las 5 primeras."
- "Está muy cargado. Quita el 30% del movimiento y deja solo lo que guía la mirada."
- **Si un arreglo no se sostiene:** "Captura p 0.48 y p 0.52 lado a lado, lista cada diferencia, encuentra la línea que la causa y arregla solo esa línea."

**Una o dos notas por ronda.** Pegar siete a la vez convierte un arreglo en una reescritura.

### Traducción de feedback del cliente a números
| Lo que dicen | Lo que se hace |
|---|---|
| "Que haga pop" | escala 1.0 → 1.08 → 1.0 en 100 ms, pico en el evento |
| "Que se vea premium" | `ease.premium` en entradas, resorte zeta 0.8, sin overshoot en el texto |
| "Se arrastra" | acortar el pin 25% |
| "Está muy cargado" | un protagonista; el resto +150 ms al 60% del recorrido |
| "Se ve hecho con IA" | listar por nombre los defaults usados, agregarlos a BANNED y rehacer |

### Definición de "listo" por escena
- [ ] Brief completo en `/briefs/<id>.md`
- [ ] Registrada en `window.__sections` y congelable con `?s=<id>&p=`
- [ ] Capturas desktop + móvil en los 5 valores de `p`, revisadas con notas escritas
- [ ] Un solo protagonista; el texto fijo mientras se lee
- [ ] Solo tokens de `motion.js`, sin números sueltos
- [ ] Nada de la lista BANNED
- [ ] Contraste ≥ 4.5:1 en todos los `p`; funciona con `prefers-reduced-motion`
- [ ] 60 fps en el perfil de Performance

---

## 11. Registro de fallas → arreglo (memoria del equipo)

| Síntoma | Arreglo |
|---|---|
| Parpadeo o jitter | Todo como función pura de `p` o `t`. `rng(seed)` en vez de `Math.random`. Quitar timers y transiciones CSS. |
| Fuente equivocada o fallback | `font-display: block` + esperar `document.fonts.ready` antes de medir. |
| Salto en la costura del loop | Renderizar 0 a N-1. Fase = frame / N con ciclos enteros. |
| Jank al hacer scroll | Solo `transform` y `opacity`. `will-change` solo en el protagonista durante su rango. |
| Texto borroso o que tiembla | Texto fijo en píxeles enteros. |
| El texto se mueve antes de poder leerlo | Hold ≥ 0.3 s por palabra + 0.5 s (≥ 40vh de scroll quieto). |
| Todo se mueve a la vez | Un protagonista; el resto +150 ms al 60%. |
| Banding en gradientes | Agregar dither (ruido 1–2% con semilla) o usar colores planos. |
| La escena se ve distinta al volver a scrollear hacia arriba | Hay estado acumulado: mover todo a `render(p)`. |
| _(agregar aquí cada falla nueva con su arreglo)_ | |

Cuando un arreglo funciona, se agrega aquí. **Este archivo es la memoria del equipo: cada línea es una falla que nadie tiene que volver a ver.**
