#ifndef IFORCE2D_INVERTED_PENDULUM2_H
#define IFORCE2D_INVERTED_PENDULUM2_H

#include <vector>
#include "PIDController.h"
using namespace std;

#ifndef DEGTORAD
#define DEGTORAD 0.0174532925199432957f
#define RADTODEG 57.295779513082320876f
#endif

#define PENDULUM_LENGTH 10

class iforce2d_invertedPendulum2 : public Test
{
public:
    iforce2d_invertedPendulum2()
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

        // 'cart' with two wheels
        {
            b2PolygonShape shape;
            shape.SetAsBox(2, 1);

            b2BodyDef bd;
            bd.type = b2_dynamicBody;
            bd.position.Set(0, 2);
            m_cartBody = m_world->CreateBody(&bd);
            m_cartBody->CreateFixture(&shape, 10.0f);

            b2CircleShape circleShape;
            circleShape.m_radius = 1;

            b2FixtureDef fd;
            fd.shape = &circleShape;
            fd.density = 10;
            fd.friction = 1;

            bd.position.Set(-2, 1);
            b2Body* leftWheelBody = m_world->CreateBody(&bd);
            leftWheelBody->CreateFixture(&fd);

            bd.position.Set( 2, 1);
            b2Body* rightWheelBody = m_world->CreateBody(&bd);
            rightWheelBody->CreateFixture(&fd);

            b2RevoluteJointDef jd;
            jd.bodyA = m_cartBody;
            jd.bodyB = leftWheelBody;
            jd.localAnchorA.Set(-2,-1);
            jd.localAnchorB.Set(0,0);
            m_wheelJoints[0] = (b2RevoluteJoint*)m_world->CreateJoint(&jd);

            jd.bodyB = rightWheelBody;
            jd.localAnchorA.Set( 2,-1);
            m_wheelJoints[1] = (b2RevoluteJoint*)m_world->CreateJoint(&jd);

            for (int i = 0; i < 2; i++) {
                m_wheelJoints[i]->EnableMotor(true);
                m_wheelJoints[i]->SetMaxMotorTorque(1500);
            }
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

        m_angleController.setGains( 1000, 0, 250 );
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

        if ( true ) {
            m_posAvg = 0.95 * m_posAvg + 0.05 * m_pendulumBody->GetPosition().x;

            m_positionController.setError( m_targetPosition - m_posAvg );
            m_positionController.step( 1 / settings->hz );
            float targetLinAccel = m_positionController.getOutput();
            targetLinAccel = b2Clamp(targetLinAccel, -10.0f, 10.0f);

            targetAngle = targetLinAccel / m_world->GetGravity().y;
            targetAngle = b2Clamp(targetAngle, -12 * DEGTORAD, 12 * DEGTORAD);
        }

        float currentAngle = m_pendulumBody->GetAngle();
        normalizeAngle(currentAngle);
        m_angleController.setError( targetAngle - currentAngle );
        m_angleController.step( 1 / settings->hz );
        float targetSpeed = m_angleController.getOutput();

        if ( fabsf(targetSpeed) > 1000 )
            targetSpeed = 0;

        float targetAngularVelocity = -targetSpeed / (2 * M_PI * 1); // wheel circumference = 2*pi*r

        for (int i = 0; i < 2; i++)
            m_wheelJoints[i]->SetMotorSpeed(targetAngularVelocity);
    }

	static Test* Create()
	{
        return new iforce2d_invertedPendulum2;
	}

    b2Body* m_cartBody;
    b2Body* m_pendulumBody;
    b2RevoluteJoint* m_pendulumJoint;
    b2RevoluteJoint* m_wheelJoints[2];

    PIDController m_angleController;
    PIDController m_positionController;

    float m_targetPosition;
    float m_posAvg;
};

#endif
