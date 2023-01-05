import { test, expect } from '@playwright/test';

test('api', async ({ page }) => {
  await page.goto('http://localhost:3000/xxx/view/844424930140110');

  // Wait for loading
  await expect(page).toHaveTitle(/First Post/);

  await page.getByAltText('Reply to root').click();

  await page.getByPlaceholder('Write here...').type('Make this');

  await page.getByText('Submit').click();

  // Arriving text
});
