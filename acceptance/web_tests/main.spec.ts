import { test, expect } from '@playwright/test';

test('api', async ({ page }) => {
  await page.goto('');

  // Wait for loading
  await expect(page).toHaveTitle(/First Post/);

  await page.getByAltText('Reply to root').click();

  await page.getByPlaceholder('Write here...').type('Make this');

  await page.getByText('Submit').click();

  // Arriving text
});
