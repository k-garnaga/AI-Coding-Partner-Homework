const request = require('supertest');

const app = require('../server');

describe('Users API - GET /api/users/:id', () => {
  test('returns 200 and the user when id exists', async () => {
    const res = await request(app).get('/api/users/123');

    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({ id: 123, name: expect.any(String), email: expect.any(String) });
  });

  test('returns 404 when id is a valid integer but user does not exist', async () => {
    const res = await request(app).get('/api/users/999');

    expect(res.status).toBe(404);
    expect(res.body).toEqual({ error: 'User not found' });
  });

  test('returns 400 when id is not a valid integer', async () => {
    const res = await request(app).get('/api/users/abc');

    expect(res.status).toBe(400);
    expect(res.body).toEqual({ error: 'Invalid user id' });
  });
});
