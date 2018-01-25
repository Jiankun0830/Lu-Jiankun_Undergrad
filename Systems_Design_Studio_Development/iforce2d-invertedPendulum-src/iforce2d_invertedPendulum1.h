#ifndef IFORCE2D_INVERTED_PENDULUM_H
#define IFORCE2D_INVERTED_PENDULUM_H

#include <vector>
#include "PIDController.h"
using namespace std;

#ifndef DEGTORAD
#define DEGTORAD 0.0174532925199432957f
#define RADTODEG 57.295779513082320876f
#endif

#define PENDULUM_LENGTH 10

class iforce2d_invertedPendulum1 : public Test
{
public:
    iforce2d_invertedPendulum1()
    {
        m_world->SetGravity( b2Vec2(0, -30) );

        //ground
		b2Body* ground = NULL;
		{
			b2BodyDef bd;
			ground = m_world->CreateBody(&bd);

            b2EdgeShape edgeShape;
            edgeShape.Set(b2Vec2(-100.0f, 0.0f), b2Vec2(100.0f, 0.0f));
            b2FixtureDef fd;
            fd.shape = &edgeShape;
            fd.density = 1;
            fd.friction = 1;
            ground->CreateFixture(&fd);
		}

        // 'cart' with prismatic constraint
        {
            b2PolygonShape shape;
            shape.SetAsBox(1, 1);

            b2BodyDef bd;
            bd.type = b2_dynamicBody;
            bd.position.Set(0, 2);
            m_cartBody = m_world->CreateBody(&bd);
            m_cartBody->CreateFixture(&shape, 1.0f);

            b2PrismaticJointDef jd;
            jd.bodyA = ground;
            jd.bodyB = m_cartBody;
            jd.localAnchorA.Set(0,2);
            jd.localAnchorB.Set(0,0);
            jd.localAxisA.Set(1,0);
            jd.motorSpeed = 0;
            jd.maxMotorForce = 1000.0f;
            jd.enableMotor = true;
            m_prismaticJoint = (b2PrismaticJoint*)m_world->CreateJoint(&jd);
        }

        //pendulum
        {
            b2PolygonShape shape;
            shape.SetAsBox(0.5, 0.5 * PENDULUM_LENGTH);

            b2BodyDef bd;
            bd.type = b2_dynamicBody;
            bd.position.Set(0, 2 + 0.5 * PENDULUM_LENGTH);
            m_pendulumBody = m_world->CreateBody(&bd);
            m_pendulumBody->CreateFixture(&shape, 1.0f);

            b2RevoluteJointDef jd;
            jd.bodyA = m_cartBody;
            jd.bodyB = m_pendulumBody;
            jd.localAnchorA.Set(0,0);
            jd.localAnchorB.Set(0,-0.5 * PENDULUM_LENGTH);
            m_pendulumJoint = (b2RevoluteJoint*)m_world->CreateJoint(&jd);
        }

        m_angleController.setGains( 1000, 0, 50 );
        m_positionController.setGains( 1.0, 0.0, 1.5 );
        m_positionController.setGains( 0.5, 0.0, 1.5 );

        m_targetPosition = 0;
        m_posAvg = 0;
    }

    void normalizeAngle(float& angle) {
        while (angle >  180 * DEGTORAD) angle -= 360 * DEGTORAD;
        while (angle < -180 * DEGTORAD) angle += 360 * DEGTORAD;
    }

    void Keyboard(unsigned char key)
    {
        switch (key)
        {
        case '1': m_targetPosition = -20; break;
        case '2': m_targetPosition =   0; break;
        case '3': m_targetPosition =  20; break;
        }
    }

	void Step(Settings* settings)
    {
		Test::Step(settings);

        //draw target position marker
        glColor3f(1,0,0);
        glBegin(GL_LINES);
        glVertex2f(m_targetPosition,-1);
        glVertex2f(m_targetPosition,-2);
        glEnd();

        m_debugDraw.DrawString(5, m_textLine, "Press 1/2/3 to move target position");
        m_textLine += DRAW_STRING_NEW_LINE;

        float targetAngle = 0;

        if ( true ) { // bring pendulum back to center
            m_posAvg = 0.95 * m_posAvg + 0.05 * m_pendulumBody->GetPosition().x;

            m_positionController.setError( m_targetPosition - m_posAvg );
            m_positionController.step( 1 / settings->hz );
            float targetLinAccel = m_positionController.getOutput();

            targetLinAccel = b2Clamp(targetLinAccel, -10.0f, 10.0f);
            targetAngle = targetLinAccel / m_world->GetGravity().y;
        }

        float currentAngle = m_pendulumBody->GetAngle();
        normalizeAngle(currentAngle);
        m_angleController.setError( targetAngle - currentAngle );
        m_angleController.step( 1 / settings->hz );
        float targetSpeed = m_angleController.getOutput();

        // give up if speed required is really high
        if ( fabsf(targetSpeed) > 1200 )
            targetSpeed = 0;

        // this is the only output
        m_prismaticJoint->SetMotorSpeed( targetSpeed );
	}

	static Test* Create()
	{
        return new iforce2d_invertedPendulum1;
	}

    b2Body* m_cartBody;
    b2PrismaticJoint* m_prismaticJoint;

    b2Body* m_pendulumBody;
    b2RevoluteJoint* m_pendulumJoint;

    PIDController m_angleController;
    PIDController m_positionController;

    float m_targetPosition;
    float m_posAvg;
};

#endif
