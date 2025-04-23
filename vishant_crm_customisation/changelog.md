## [18.0.1.0.0] - 2025-04-18

### Added
- Introduced a new field `job_name` in the following models:
  - `sale.order`
  - `project.project`
  - `account.move`
  - `mrp.production`
  - `purchase.order`
  - `stock.move`

### Changed
- The `job_name` field is now propagated from the `sale.order` to the following related documents:
  - Manufacturing Order (`mrp.production`)
  - Purchase Order (`purchase.order`)
  - Delivery Order (`stock.move`)
  - Invoice (`account.move`)
  - Project (`project.project`)

### Notes
- In the `sale.order`, the `job_name` field is automatically derived from the related CRM Lead name.
