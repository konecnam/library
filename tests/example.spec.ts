import { test, expect, Page } from '@playwright/test';
import Database from 'better-sqlite3';

test.beforeEach(async () => {
  const db = new Database('db.sqlite3');
  db.prepare("delete from library_mybook where created_by_id in (select id from library_user where username Like 'Test_%')").run();
  db.prepare("delete FROM library_user where username like 'Test_%'").run();
  db.close();
});

test.afterEach(async () => {
  
});

export async function create_user(
  username: string, 
  email: string,
  password: string='pbkdf2_sha256$600000$r7tZGq5YwfY04L3sfNlsiy$dOniI3/GDTMlghHAW2PRh4y9ol7+xuCo3kcEuj+4X6Y=' 

){
  const db = new Database('db.sqlite3');
  const stmt = db.prepare(`
    INSERT INTO library_user (password, username, email, is_superuser, first_name, last_name, is_staff, is_active, date_joined) VALUES (?, ?, ?, 0, '', '', 1, 1, '2026-02-01')
    `);
   stmt.run(
    password,
    username,
    email
  );
  db.close();
}

export async function login(
  page: Page,
  username:string,
): Promise<void>{
  await page.goto('http://127.0.0.1:8000');
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[1]').click();
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="password"]').fill('heslo');
  await page.locator('xpath=/html/body/div/div/main/div/div/form/input[2]').click();

}


export async function create_book(
  username:string,
  book_title: string, 
  author: string,
  book_description: string, 
  image: string, 
  category: string, 
  date: string='2026-02-01'

){
  const db = new Database('db.sqlite3');
  const stmt = db.prepare(`
    INSERT INTO library_mybook (created_by_id, book_title, author, book_description, image, category, date) VALUES ((select id from library_user where username= ?), ?, ?, ?, ?, ?, ?)
    `);
   stmt.run(
    username,
    book_title,
    author, 
    book_description,
    image, 
    category, 
    date
  );
  db.close();
}


test('User registration flow', async ({ page }) => {
  await page.goto('http://127.0.0.1:8000');
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

 
  const title = await page.locator('xpath=/html/body/div/div/main/div/div/h2');
  await expect(title).toHaveText('Register');

  const username = 'Test_Mato';
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="email"]').fill('mato9@google.com');
  await page.locator('input[name="password"]').fill('mybook8');
  await page.locator('input[name="confirmation"]').fill('mybook8');

  await page.locator('xpath=/html/body/div/div/main/div/div/form/input[2]').click();
  
  const title_besst_seller = await page.locator('xpath=/html/body/div/div/main/div/h4');
  await expect(title_besst_seller).toHaveText('Best sellers');
});

test ('Exist user registration flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')

  await page.goto('http://127.0.0.1:8000');
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

 
  const title = await page.locator('xpath=/html/body/div/div/main/div/div/h2');
  await expect(title).toHaveText('Register');

  const username = 'Test_Laura';
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="email"]').fill('mato9@google.com');
  await page.locator('input[name="password"]').fill('mybook8');
  await page.locator('input[name="confirmation"]').fill('mybook8');

  await page.locator('xpath=/html/body/div/div/main/div/div/form/input[2]').click();
  
  const user_exist = await page.locator('xpath=//*[@id="message"]');
  await expect(user_exist).toHaveText('Username already taken.');
  });


test ('user registration false password flow', async ({ page }) => {
  await page.goto('http://127.0.0.1:8000');
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

 
  const title = await page.locator('xpath=/html/body/div/div/main/div/div/h2');
  await expect(title).toHaveText('Register');

  const username = 'Test_Laura';
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="email"]').fill('mato9@google.com');
  await page.locator('input[name="password"]').fill('mybook8');
  await page.locator('input[name="confirmation"]').fill('mybook88');

  await page.locator('xpath=/html/body/div/div/main/div/div/form/input[2]').click();
  
  const user_exist = await page.locator('xpath=//*[@id="message"]');
  await expect(user_exist).toHaveText('Passwords must match.');
  });

  test ('from registration to login flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await page.goto('http://127.0.0.1:8000');
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

  const title_register = await page.locator('xpath=/html/body/div/div/main/div/div/h2');
  await expect(title_register).toHaveText('Register');
  await page.locator('xpath=/html/body/div/div/main/div/div/a').click();
  const title_login = await page.locator('xpath=/html/body/div/div/main/div/div/h2');
  await expect(title_login).toHaveText('Login');

  await page.locator('input[name="username"]').fill('Test_Laura');
  await page.locator('input[name="password"]').fill('heslo');
  await page.locator('xpath=/html/body/div/div/main/div/div/form/input[2]').click();
  
  const title_besst_seller = await page.locator('xpath=/html/body/div/div/main/div/h4');
  await expect(title_besst_seller).toHaveText('Best sellers');
});

test ('from login to registration flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await page.goto('http://127.0.0.1:8000');
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[1]').click();

  const title_register = await page.locator('xpath=/html/body/div/div/main/div/div/h2');
  await expect(title_register).toHaveText('Login');
  await page.locator('xpath=/html/body/div/div/main/div/div/a').click();
  const title_login = await page.locator('xpath=/html/body/div/div/main/div/div/h2');
  await expect(title_login).toHaveText('Register');
});


test ('add book collection and saved book flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await login(page, 'Test_Laura')
  const title_besst_seller = await page.locator('xpath=/html/body/div/div/main/div/h4');
  await expect(title_besst_seller).toHaveText('Best sellers');
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();
  await page.locator('xpath=/html/body/div/div/main/div/div[1]/button/span').click();

  await page.fill('xpath=/html/body/div/div/main/div/form[1]/div[1]/input', 'The Fake Out');
  await page.fill('xpath=/html/body/div/div/main/div/form[1]/div[2]/input', 'Stephanie Archer');
  await page.fill('xpath=/html/body/div/div/main/div/form[1]/div[3]/textarea', 'The best way to get back at my horrible ex?');
  await page.fill('xpath=/html/body/div/div/main/div/form[1]/div[4]/input', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/641818923/gardnes-9781398724280.jpg');
  await page.selectOption('xpath=/html/body/div/div/main/div/form[1]/div[5]/select', {label: 'Romantic'});
  await page.locator('xpath=/html/body/div/div/main/div/form[1]/input[2]').click();
  
  const title_saved_book = await page.locator('xpath=/html/body/div/div/main/div/h4[2]');
  await expect(title_saved_book).toHaveText('Saved Books');

  const title_book_saved = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/h5[1]');
  await expect(title_book_saved).toHaveText('The Fake Out');

  const author_book_saved = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/h5[2]');
  await expect(author_book_saved).toHaveText('Stephanie Archer');

  const description_saved_book = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/p[1]');
  await expect(description_saved_book).toHaveText('Book description: The best way to get back at my horrible ex?');
  const category_saved_book = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/p[2]');
  await expect(category_saved_book).toHaveText('Category: Romantic');
})


test ('edit saved book author, name, description flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'Behind The Net', 'Mona Kasten', 'He is the hot, grumpy goalie I had a crush on in high school... and now I am his live-in assistant.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/641818923/gardnes-9781398724280.jpg', 'Romantic' );
  await login(page, 'Test_Laura')
  const title_besst_seller = await page.locator('xpath=/html/body/div/div/main/div/h4');
  await expect(title_besst_seller).toHaveText('Best sellers');
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

  await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/div/button').click();

  const title_change_input = page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/form[1]/div[1]/input');
  await expect(title_change_input).toBeVisible();
  await title_change_input.fill('The Fake Out');
  const author_change_input = page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/form[1]/div[2]/input');
  await expect(author_change_input).toBeVisible();
  await author_change_input.fill('Stephanie Archer');
  const description_change_input = page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/form[1]/div[3]/input');
  await expect(description_change_input).toBeVisible();
  await description_change_input.fill('The best way to get back at my horrible ex?');
  
  await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/form[1]/button[1]').click();

  const title_book_saved = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/h5[1]');
  await expect(title_book_saved).toHaveText('The Fake Out');
  const author_book_saved = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/h5[2]');
  await expect(author_book_saved).toHaveText('Stephanie Archer');
  const description_saved_book = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/p[1]');
  await expect(description_saved_book).toHaveText('Book description: The best way to get back at my horrible ex?');
 
})

test ('edit saved book category flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'The Fake Out', 'Stephanie Archer', ' The best way to get back at my horrible ex?', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/641818923/gardnes-9781398724280.jpg', 'Fantasy' );
  await login(page, 'Test_Laura')
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();
  await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/div/button').click();

  await page.selectOption('xpath=/html/body/div/div/main/div/div[2]/div/div[2]/form[1]/div[4]/select', {label: 'Romantic'});
  await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/form[1]/button[1]').click();

  const category_saved_book = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/p[2]');
  await expect(category_saved_book).toHaveText('Category: Romantic');
})

test ('edit cancel saved book flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'The Fake Out', 'Stephanie Archer', ' The best way to get back at my horrible ex?', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/641818923/gardnes-9781398724280.jpg', 'Romantic' );
  await login(page, 'Test_Laura')
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();
  await page.locator('xpath= /html/body/div/div/main/div/div[2]/div/div[2]/div/div/button').click();
  await page.locator('xpath=/html/body/div/div/main/div/div[2]/div/div[2]/form[1]/button[2]').click();

  const category_saved_book = await page.locator('xpath=/html/body/div/div/main/div/div/div/div[2]/div/p[2]');
  await expect(category_saved_book).toHaveText('Category: Romantic');
})

test ('dustbin saved book flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'The Fake Out', 'Stephanie Archer', ' The best way to get back at my horrible ex?', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/641818923/gardnes-9781398724280.jpg', 'Romantic', '2026-01-01');

  await create_book('Test_Laura', 'Spiral', 'Bal Khabra', ' He is on edge while she is en pointe in this fake-dating sports romance from the author of the smash hit Collide.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/s/spiral-9781526677884.jpg', 'Romantic', '2026-02-01' );
  await login(page, 'Test_Laura')
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

  const title_book_saved_spiral = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]');
  await expect(title_book_saved_spiral).toHaveText('Spiral');

  const title_book_saved_fake_out = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[2]/div[2]/div/h5[1]');
  await expect(title_book_saved_fake_out).toHaveText('The Fake Out');

  await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/div/form/button/i').click();
  const title_book_saved = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]');
  await expect(title_book_saved).toHaveText('The Fake Out'); 
})

test ('search by author flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'The Fake Out', 'Stephanie Archer', ' The best way to get back at my horrible ex?', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/641818923/gardnes-9781398724280.jpg', 'Romantic', '2026-01-01');

  await create_book('Test_Laura', 'Spiral', 'Bal Khabra', ' He is on edge while she is en pointe in this fake-dating sports romance from the author of the smash hit Collide.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/s/spiral-9781526677884.jpg', 'Romantic', '2026-02-01' );

  await create_book('Test_Laura', 'Collide', 'Bal Khabra', 'When Summer Preston is professor issues her with an ultimatum, she finds herself on an unexpected collision course with hockey captain.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/682457503/collide.jpg', 'Romantic', '2025-03-01' );
  await login(page, 'Test_Laura')
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

  await page.fill('xpath=/html/body/div/div/main/div/form/div/div/input', 'Khabra');
  await page.locator('xpath=/html/body/div/div/main/div/form/button').click();

  const title_book_saved_spiral = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]');
  await expect(title_book_saved_spiral).toHaveText('Spiral');

  const title_book_saved_fake_out = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[2]/div[2]/div/h5[1]');
  await expect(title_book_saved_fake_out).toHaveText('Collide');
})

test ('search by author or title flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'Harry Potter and the Goblet of Fire', 'Joanne K. Rowlingová', 'Loved by millions of readers worldwide,', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/h/harry-potter-and-the-goblet-of-fire-9781408855683_38.jpg', 'Fantasy', '2021-01-01');

  await create_book('Test_Laura', 'Harry Potter and the Prisoner of Azkaban', 'Joanne K. Rowlingová', 'Loved by millions of readers worldwide.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/627492/gardnes-9781408855676.jpg', 'Fantasy', '2019-02-01' );

  await create_book('Test_Laura', 'The Deathworld Omnibus', 'Harry Harrison', 'The planet was called Pyrrus, a strange place where all the beasts', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/495003783/the-deathworld-omnibus-1-3.jpg', 'Other', '2020-03-01' );

  await create_book('Test_Laura', 'Collide', 'Bal Khabra', 'When Summer Preston’s professor issues her with an ultimatum, she finds herself on an unexpected collision course with hockey captain.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/682457503/collide.jpg', 'Romantic', '2025-03-01' );
  await login(page, 'Test_Laura')
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

  await page.fill('xpath=/html/body/div/div/main/div/form/div/div/input', 'harry');
  await page.locator('xpath=/html/body/div/div/main/div/form/button').click();

  const title_book_saved_Harry_3 = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]');
  await expect(title_book_saved_Harry_3).toHaveText('Harry Potter and the Goblet of Fire');

  const title_book_saved_omnibus = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[2]/div[2]/div/h5[1]');
  await expect(title_book_saved_omnibus).toHaveText('The Deathworld Omnibus');

  const title_book_saved_Harry_4 = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[3]/div[2]/div/h5[1]');
  await expect(title_book_saved_Harry_4).toHaveText('Harry Potter and the Prisoner of Azkaban');
  
})

test ('no search flow', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'Collide', 'Bal Khabra', 'When Summer Preston’s professor issues her with an ultimatum, she finds herself on an unexpected collision course with hockey captain.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/682457503/collide.jpg', 'Romantic', '2025-03-01' );
  await login(page, 'Test_Laura')
  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();

  await page.fill('xpath=/html/body/div/div/main/div/form/div/div/input', 'while ');
  await page.locator('xpath=/html/body/div/div/main/div/form/button').click();
  const title_book_saved = await page.locator('xpath=/html/body/div/div/main/div/div[2]/h5');
  await expect(title_book_saved).toHaveText('No books saved yet.');   
})

test ('saved book button dvo next one', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'Collide', 'Bal Khabra', 'When Summer Preston’s professor issues her with an ultimatum, she finds herself on an unexpected collision course with hockey captain.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/682457503/collide.jpg', 'Romantic', '2023-03-01' );
  for (let i = 0; i < 7; i++){
    await create_book('Test_Laura', 'Spiral', 'Bal Khabra', ' He is on edge while she is en pointe in this fake-dating sports romance from the author of the smash hit Collide.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/s/spiral-9781526677884.jpg', 'Romantic', '2024-02-01' );
  }

  await create_book('Test_Laura', 'The Fake Out', 'Stephanie Archer', ' The best way to get back at my horrible ex?', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/641818923/gardnes-9781398724280.jpg', 'Romantic', '2026-01-01');
  await login(page, 'Test_Laura')

  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();
  await page.locator('xpath=/html/body/div/div/main/div/div[2]/nav/ul/li[2]/a').click();
  const title_book_saved_collide = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div/div[2]/div/h5[1]');
  await expect(title_book_saved_collide).toHaveText('Collide');

  await page.locator('xpath=/html/body/div/div/main/div/div[2]/nav/ul/li[1]/a').click();
  const title_book_saved_fake_out = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]');
  await expect(title_book_saved_fake_out).toHaveText('The Fake Out'); 
});

test ('saved book next_previous', async ({ page }) => {
  await create_user ('Test_Laura', 'laura@gmail.com')
  await create_book('Test_Laura', 'Collide', 'Bal Khabra', 'When Summer Preston’s professor issues her with an ultimatum, she finds herself on an unexpected collision course with hockey captain.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/682457503/collide.jpg', 'Romantic', '2023-03-01' );
  for (let i = 0; i < 15; i++){
    await create_book('Test_Laura', 'Spiral', 'Bal Khabra', ' He is on edge while she is en pointe in this fake-dating sports romance from the author of the smash hit Collide.', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/s/spiral-9781526677884.jpg', 'Romantic', '2024-02-01' );
  }

  await create_book('Test_Laura', 'The Fake Out', 'Stephanie Archer', ' The best way to get back at my horrible ex?', 'https://www.knihydobrovsky.cz/thumbs/book-detail-fancy-box/mod_eshop/produkty/641818923/gardnes-9781398724280.jpg', 'Romantic', '2026-01-01');
  await login(page, 'Test_Laura')

  await page.locator('xpath=/html/body/div/div/header/div[2]/nav/a[2]').click();
  await page.locator('xpath=/html/body/div/div/main/div/div[2]/nav/ul/a').click();
  await page.locator('xpath=/html/body/div/div/main/div/div[2]/nav/ul/a').click();
  const title_book_saved_collide = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div/div[2]/div/h5[1]');
  await expect(title_book_saved_collide).toHaveText('Collide');

  await page.locator('xpath=/html/body/div/div/main/div/div[2]/nav/ul/li[1]/a').click();
  await page.locator('xpath=/html/body/div/div/main/div/div[2]/nav/ul/li[1]/a').click();
  const title_book_saved_fake_out = await page.locator('xpath=/html/body/div/div/main/div/div[2]/div[1]/div[2]/div/h5[1]');
  await expect(title_book_saved_fake_out).toHaveText('The Fake Out'); 
});


  