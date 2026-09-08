---
name: angular
description: Modern Angular (v20+) expert with deep knowledge of Signals, Standalone Components, Zoneless applications, SSR/Hydration, and reactive patterns.
risk: safe
source: self
date_added: '2026-02-27'
---

# Angular Expert

Master modern Angular development with Signals, Standalone Components, Zoneless applications, SSR/Hydration, and the latest reactive patterns.

## When to Use This Skill

- Building new Angular applications (v20+)
- Implementing Signals-based reactive patterns
- Creating Standalone Components and migrating from NgModules
- Configuring Zoneless Angular applications
- Implementing SSR, prerendering, and hydration
- Optimizing Angular performance
- Adopting modern Angular patterns and best practices

## Do Not Use This Skill When

- Migrating from AngularJS (1.x) → use `angular-migration` skill
- Working with legacy Angular apps that cannot upgrade
- General TypeScript issues → use `typescript-expert` skill

## Instructions

1. Assess the Angular version and project structure
2. Apply modern patterns (Signals, Standalone, Zoneless)
3. Implement with proper typing and reactivity
4. Validate with build and tests

## Safety

- Always test changes in development before production
- Gradual migration for existing apps (don't big-bang refactor)
- Keep backward compatibility during transitions

---

## Angular Version Timeline

| Version        | Release | Key Features                                           |
| -------------- | ------- | ------------------------------------------------------ |
| **Angular 20** | Q2 2025 | Signals stable, Zoneless stable, Incremental hydration |
| **Angular 21** | Q4 2025 | Signals-first default, Enhanced SSR                    |
| **Angular 22** | Q2 2026 | Signal Forms, Selectorless components                  |

---

## 1. Signals: The New Reactive Primitive

Signals are Angular's fine-grained reactivity system, replacing zone.js-based change detection.

### Core Concepts

```typescript
import { signal, computed, effect } from "@angular/core";

// Writable signal
const count = signal(0);

// Read value
console.log(count()); // 0

// Update value
count.set(5); // Direct set
count.update((v) => v + 1); // Functional update

// Computed (derived) signal
const doubled = computed(() => count() * 2);

// Effect (side effects)
effect(() => {
  console.log(`Count changed to: ${count()}`);
});
```

### Signal-Based Inputs and Outputs

```typescript
import { Component, input, output, model } from "@angular/core";

@Component({
  selector: "app-user-card",
  standalone: true,
  template: `
    <div class="card">
      <h3>{{ name() }}</h3>
      <span>{{ role() }}</span>
      <button (click)="select.emit(id())">Select</button>
    </div>
  `,
})
export class UserCardComponent {
  // Signal inputs (read-only)
  id = input.required<string>();
  name = input.required<string>();
  role = input<string>("User"); // With default

  // Output
  select = output<string>();

  // Two-way binding (model)
  isSelected = model(false);
}

// Usage:
// <app-user-card [id]="'123'" [name]="'John'" [(isSelected)]="selected" />
```

### Signal Queries (ViewChild/ContentChild)

```typescript
import {
  Component,
  viewChild,
  viewChildren,
  contentChild,
} from "@angular/core";

@Component({
  selector: "app-container",
  standalone: true,
  template: `
    <input #searchInput />
    <app-item *ngFor="let item of items()" />
  `,
})
export class ContainerComponent {
  // Signal-based queries
  searchInput = viewChild<ElementRef>("searchInput");
  items = viewChildren(ItemComponent);
  projectedContent = contentChild(HeaderDirective);

  focusSearch() {
    this.searchInput()?.nativeElement.focus();
  }
}
```

### When to Use Signals vs RxJS

| Use Case                | Signals         | RxJS                             |
| ----------------------- | --------------- | -------------------------------- |
| Local component state   | ✅ Preferred    | Overkill                         |
| Derived/computed values | ✅ Preferred    | Possible via map/combineLatest   |
| Async operations        | ❌ Not designed | ✅ Preferred (switchMap, etc.)   |
| Event streams           | ❌ Not designed | ✅ Preferred (Subject, fromEvent)|
| HTTP requests           | ❌ Not designed | ✅ Preferred (HttpClient streams)|

### Signal Interop with RxJS

```typescript
import { toSignal, toObservable } from "@angular/core/rxjs-interop";

// RxJS Observable → Signal
const user$ = this.userService.getUsers();
const users = toSignal(user$, { initialValue: [] });

// Signal → RxJS Observable
const count$ = toObservable(this.count);

// Using with pipe
import { takeUntilDestroyed } from "@angular/core/rxjs-interop";

@Component({ standalone: true })
export class MyComponent {
  private destroyRef = inject(DestroyRef);

  ngOnInit() {
    interval(1000)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((n) => this.count.set(n));
  }
}
```

---

## 2. Standalone Components (Default in Angular 20+)

### Module-Free Architecture

```typescript
import { Component } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";

@Component({
  selector: "app-standalone-demo",
  standalone: true,
  imports: [CommonModule, FormsModule], // Direct imports
  template: `
    <h2>Standalone Component</h2>
    <input [(ngModel)]="name" />
    <p *ngIf="name">{{ name }}</p>
  `,
})
export class StandaloneDemoComponent {
  name = "";
}
```

### bootstrapApplication (No AppModule)

```typescript
import { bootstrapApplication } from "@angular/platform-browser";
import { provideRouter } from "@angular/router";
import { provideHttpClient } from "@angular/common/http";
import { AppComponent } from "./app/app.component";
import { routes } from "./app/app.routes";

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
  ],
}).catch((err) => console.error(err));
```

### Migrating from NgModules

```typescript
// OLD: NgModule
@NgModule({
  declarations: [ComponentA, ComponentB],
  imports: [SharedModule],
  providers: [MyService],
})
export class FeatureModule {}

// NEW: Standalone
@Component({
  standalone: true,
  imports: [SharedModule], // Still works for gradual migration
})
export class ComponentA {}

// Use providers with inject() or provideIn: 'root'
@Injectable({ providedIn: "root" })
export class MyService {}
```

---

## 3. Zoneless Angular

### Enabling Zoneless

```typescript
import { bootstrapApplication } from "@angular/platform-browser";
import { provideExperimentalZonelessChangeDetection } from "@angular/core";

bootstrapApplication(AppComponent, {
  providers: [
    provideExperimentalZonelessChangeDetection(),
  ],
});
```

### How Change Detection Works Without Zone.js

- Angular subscribes to Signal changes directly
- `markForCheck()` triggers CD manually
- AsyncPipe triggers CD through internal subscription
- Event binding triggers CD by Angular internal notification

### Zoneless Considerations

```typescript
// ✅ These trigger change detection in Zoneless
@Component({ standalone: true, changeDetection: ChangeDetectionStrategy.OnPush })
export class ZonelessComponent {
  count = signal(0); // Signal: auto-triggers CD

  increment() {
    this.count.update(v => v + 1); // Triggers CD
  }
}

// ❌ These DON'T trigger CD in Zoneless
export class BadComponent {
  count = 0; // Plain property: NO CD trigger

  increment() {
    this.count++; // Won't update UI without Signal/manual trigger
  }
}
```

---

## 4. New Control Flow Syntax (@if, @for, @switch)

```typescript
@Component({
  standalone: true,
  template: `
    @if (isLoggedIn()) {
      <app-dashboard [user]="currentUser()" />
    } @else {
      <app-login (loginSuccess)="handleLogin()" />
    }

    @for (item of items(); track item.id) {
      <app-item-card [item]="item" />
    } @empty {
      <p>No items found</p>
    }

    @switch (status()) {
      @case ("loading") { <app-spinner /> }
      @case ("error") { <app-error [message]="errorMsg()" /> }
      @case ("success") { <app-data [data]="result()" /> }
      @default { <app-empty /> }
    }
  `,
})
export class ModernTemplateComponent {}
```

---

## 5. Deferrable Views (@defer)

```typescript
@Component({
  standalone: true,
  template: `
    @defer (on viewport) {
      <app-heavy-chart [data]="chartData()" />
    } @placeholder {
      <div class="placeholder">Chart area</div>
    } @loading (minimum 1s) {
      <app-spinner />
    } @error {
      <app-error message="Failed to load chart" />
    }

    @defer (on interaction) {
      <app-comments [postId]="id()" />
    } @placeholder {
      <button>Show Comments</button>
    }

    @defer (on hover; prefetch on idle) {
      <app-large-media [src]="mediaUrl()" />
    } @placeholder {
      <div class="media-placeholder">Hover to load</div>
    }
  `,
})
export class DeferDemoComponent {}
```

---

## 6. Dependency Injection with inject()

```typescript
import { Component, inject } from "@angular/core";

// Preferred: inject() function
@Component({ standalone: true })
export class UserProfileComponent {
  private userService = inject(UserService);
  private router = inject(Router);

  currentUser = this.userService.currentUser; // Signal

  navigateToSettings() {
    this.router.navigate(["/settings"]);
  }
}

// With injection tokens
import { InjectionToken } from "@angular/core";

export const API_URL = new InjectionToken<string>("API_URL");

@Component({
  standalone: true,
  providers: [{ provide: API_URL, useValue: "https://api.example.com" }],
})
export class ApiComponent {
  apiUrl = inject(API_URL); // 'https://api.example.com'
}
```

---

## 7. Routing with Standalone

```typescript
import { Routes } from "@angular/router";

export const routes: Routes = [
  {
    path: "dashboard",
    loadComponent: () =>
      import("./dashboard.component").then((m) => m.DashboardComponent),
  },
  {
    path: "settings",
    loadChildren: () =>
      import("./settings/routes").then((m) => m.SETTINGS_ROUTES),
  },
];

// Route with guards (functional)
import { inject } from "@angular/core";
import { AuthService } from "./auth.service";

const authGuard = () => {
  const auth = inject(AuthService);
  return auth.isLoggedIn() || inject(Router).navigate(["/login"]);
};

export const protectedRoutes: Routes = [
  {
    path: "admin",
    loadComponent: () => import("./admin.component"),
    canActivate: [authGuard],
  },
];
```

---

## 8. SSR, Prerendering, and Hydration

```typescript
import { ApplicationConfig } from "@angular/core";
import {
  provideClientHydration,
  withEventReplay,
} from "@angular/platform-browser";

export const appConfig: ApplicationConfig = {
  providers: [
    provideClientHydration(withEventReplay()),
  ],
};

// Hydration-friendly components
@Component({
  standalone: true,
  template: `
    <h2>{{ title() }}</h2>
    <div class="content" [innerHTML]="safeContent()"></div>
    <!-- ✅ Consistent server/client output -->
  `,
})
export class HydrationComponent {
  title = input.required<string>();
  safeContent = computed(() => this.sanitize(this.content()));
}
```

---

## 9. Performance Optimization

### Deferred Loading

```typescript
// Component-level lazy loading
const routes: Routes = [
  {
    path: "reports",
    loadComponent: () => import("./reports.component").then(m => m.ReportsComponent)
  }
];

// Template-level defer
@defer (on viewport) {
  <app-expensive-visualization />
}
```

### Image Optimization

```typescript
import { NgOptimizedImage } from "@angular/common";

@Component({
  standalone: true,
  imports: [NgOptimizedImage],
  template: `
    <img
      ngSrc="hero.jpg"
      width="800"
      height="600"
      priority
    />

    <img
      ngSrc="thumbnail.jpg"
      width="200"
      height="150"
      loading="lazy"
      placeholder="blur"
    />
  `
})
```

---

## 10. Testing Modern Angular

### Testing Signal Components

```typescript
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { CounterComponent } from "./counter.component";

describe("CounterComponent", () => {
  let component: CounterComponent;
  let fixture: ComponentFixture<CounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CounterComponent], // Standalone import
    }).compileComponents();

    fixture = TestBed.createComponent(CounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should increment count", () => {
    expect(component.count()).toBe(0);
    component.increment();
    expect(component.count()).toBe(1);
  });
});
```

### Testing with Signal Inputs

```typescript
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { ComponentRef } from "@angular/core";
import { UserCardComponent } from "./user-card.component";

describe("UserCardComponent", () => {
  let fixture: ComponentFixture<UserCardComponent>;
  let componentRef: ComponentRef<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(UserCardComponent);
    componentRef = fixture.componentRef;

    // Set signal inputs via setInput
    componentRef.setInput("id", "123");
    componentRef.setInput("name", "John Doe");

    fixture.detectChanges();
  });

  it("should display user name", () => {
    const el = fixture.nativeElement.querySelector("h3");
    expect(el.textContent).toContain("John Doe");
  });
});
```

---

## Best Practices Summary

| Pattern              | ✅ Do                          | ❌ Don't                        |
| -------------------- | ------------------------------ | ------------------------------- |
| **State**            | Use Signals for local state    | Overuse RxJS for simple state   |
| **Components**       | Standalone with direct imports | Bloated SharedModules           |
| **Change Detection** | OnPush + Signals               | Default CD everywhere           |
| **Lazy Loading**     | `@defer` and `loadComponent`   | Eager load everything           |
| **DI**               | `inject()` function            | Constructor injection (verbose) |
| **Inputs**           | `input()` signal function      | `@Input()` decorator (legacy)   |
| **Zoneless**         | Enable for new projects        | Force on legacy without testing |

---

## Resources

- [Angular.dev Documentation](https://angular.dev)
- [Angular Signals Guide](https://angular.dev/guide/signals)
- [Angular SSR Guide](https://angular.dev/guide/ssr)
- [Angular Update Guide](https://angular.dev/update-guide)
- [Angular Blog](https://blog.angular.dev)

---

## Common Troubleshooting

| Issue                          | Solution                                            |
| ------------------------------ | --------------------------------------------------- |
| Signal not updating UI         | Ensure `OnPush` + call signal as function `count()` |
| Hydration mismatch             | Check server/client content consistency             |
| Circular dependency            | Use `inject()` with `forwardRef`                    |
| Zoneless not detecting changes | Trigger via signal updates, not mutations           |
| SSR fetch fails                | Use `TransferState` or `withFetch()`                |
